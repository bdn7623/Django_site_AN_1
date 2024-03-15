from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib import messages

from blog.models import Post
from .forms import (
    RegisterForm,
    LoginForm,
    ReactivationForm,
    PasswordSetForm,
    ProfileForm
)
from .models import ActivationToken, PasswordResetToken, Profile
from .utils import send_activation_email, send_password_reset_email

User = get_user_model()


@login_required
def register_view(request):
    """
    View function for user registration.

    If the user is already authenticated, redirects to the post list page.
    Otherwise, handles the registration form submission.

    Args:
    - request: HttpRequest object.

    Returns:
    - HttpResponseRedirect or HttpResponse: If the request method is POST and the form
      is valid, redirects to the post list page after registration. If the form is invalid,
      renders the registration form again with error messages. If the request method is GET,
      renders the registration form.
    """
    if request.user.is_authenticated:
        messages.info(request, 'You already have an account')
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            user_token = ActivationToken.objects.create(user=user)
            send_activation_email(user, user_token, request)
            messages.success(request, 'You have to activate your account')
            return redirect('blog:post_list')
        else:
            context = {
                'form': form,
                'form_errors': form.errors
            }
            return render(request, 'accounts/register.html', context)

    form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def activate_account_view(request, username, token):
    """
    View function for activating user account.

    Args:
    - request: HttpRequest object.
    - username (str): Username of the user.
    - token (str): Token for activating the account.

    Returns:
    - HttpResponseRedirect: Redirects to the login page upon successful activation
      or if the token is expired. If the user is already activated, redirects to
      the post list page.
    """
    user = get_object_or_404(User, username=username)
    token = get_object_or_404(ActivationToken, user=user, token=token)

    if user.is_active:
        messages.error(request, 'User is already activated')
        return redirect('blog:post_list')

    if token.verify_token():
        user.is_active = True
        token.delete()
        user.save()

        messages.success(request, 'Activation complete')
        return redirect('accounts:login')

    messages.error(request, 'Token expired')
    return redirect('accounts:login')


@login_required
def reactivation_sent_view(request):
    """
    View function for sending reactivation email.

    Args:
    - request: HttpRequest object.

    Returns:
    - HttpResponseRedirect or HttpResponse: Redirects to the reactivation
      sent page upon successful email sending or renders the reactivation form.
    """
    if request.method == 'POST':
        form = ReactivationForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])

            if user.is_active:
                messages.warning(request, 'This account is already activated.')
                return redirect('accounts:login')

            old_token = ActivationToken.objects.filter(user=user).first()
            if old_token:
                old_token.delete()

            new_token = ActivationToken.objects.create(user=user)

            send_activation_email(user, new_token, request)
            messages.success(request, 'Reactivation token has been sent. Please check your email inbox.')
            return redirect('accounts:reactivate_sent')
        else:
            context = {'form': form, 'form_errors': form.errors}
            return render(request, 'accounts/reactivation_sent.html', context)

    form = ReactivationForm()
    return render(request, 'accounts/reactivation_sent.html', {'form': form})


@login_required
def password_reset_sent_view(request):
    """
    View function for sending password reset email.

    Args:
    - request: HttpRequest object.

    Returns:
    - HttpResponseRedirect or HttpResponse: Redirects to the password reset
      sent page upon successful email sending or renders the password reset form.
    """
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])

            if not user.is_active:
                messages.warning(request, 'This account is not activated.')
                return redirect('accounts:login')

            old_token = PasswordResetToken.objects.filter(user=user).first()
            if old_token:
                old_token.delete()

            new_token = PasswordResetToken.objects.create(user=user)

            send_password_reset_email(user, new_token, request)
            messages.success(request, 'Password reset token has been sent. Please check your email inbox.')
            return redirect('accounts:password_reset_sent')
        else:
            context = {'form': form, 'form_errors': form.errors}
            return render(request, 'accounts/password_reset_sent.html', context)

    form = PasswordResetForm()
    return render(request, 'accounts/password_reset_sent.html', {'form': form})


@login_required
def password_reset_done_view(request, username, token):
    """
    View function for resetting user password.

    Args:
    - request: HttpRequest object.
    - username (str): Username of the user.
    - token (str): Password reset token.

    Returns:
    - HttpResponseRedirect or HttpResponse: Redirects to the login page upon
      successful password reset or renders the password reset form.
    """
    user = get_object_or_404(User, username=username)
    token = get_object_or_404(PasswordResetToken, user=user, token=token)

    if request.method == 'POST':
        form = PasswordSetForm(user, data=request.POST)
        if form.is_valid():
            form.save()
            token.delete()
            messages.success(request, 'Your password has been updated.')
            return redirect('accounts:login')
        else:
            context = {'form': form, 'form_errors': form.errors}
            return render(request, 'accounts/password_reset_done.html', context)

    form = PasswordSetForm(user)
    return render(request, 'accounts/password_reset_done.html', {'form': form})


def login_view(request):
    """
    View function for user login.

    If the user is already authenticated, redirects to the post list page.
    Otherwise, processes the login form submission, authenticates the user,
    and redirects to the post list page upon successful login.

    Args:
    - request: HttpRequest object.

    Returns:
    - HttpResponseRedirect or HttpResponse: Redirects to the post list page
      upon successful login or renders the login form.
    """
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in')
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            user = authenticate(request, email=email, password=password)

            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60 * 60 * 24 * 7)

            if user is not None:
                login(request, user)
                return redirect('blog:post_list')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid form data')
            return redirect('accounts:login')

    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    View function for user logout.

    Logs out the current user and redirects to the login page.

    Args:
    - request: HttpRequest object.

    Returns:
    - HttpResponseRedirect: Redirects to the login page.
    """
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_create_view(request):
    """
    View function for creating a user profile.

    If the user already has a profile, redirects to the post list page.

    Args:
    - request: HttpRequest object.

    Returns:
    - HttpResponse: Rendered template with the profile creation form.
    """
    if hasattr(request.user, 'profile'):
        messages.info(request, 'You already have a profile')
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('blog:post_list')
        else:
            context = {
                'form': form,
                'form_errors': form.errors
            }
            return render(request, 'accounts/profile/create.html', context)

    form = ProfileForm()
    return render(request, 'accounts/profile/create.html', {'form': form})


def profile_detail_view(request, username):
    """
    View function to display user profile details.

    Args:
    - request: HttpRequest object.
    - username: Username of the profile to be displayed.

    Returns:
    - HttpResponse: Rendered template with user profile details.
    """
    profile = get_object_or_404(Profile, user__username=username)
    posts = Post.published.filter(author=profile.user)[:4]
    context = {
        'profile': profile,
        'posts': posts
    }
    return render(request, 'accounts/profile/detail.html', context)


@login_required
def profile_update_view(request, username):
    """
    View function to update user profile.

    Args:
    - request: HttpRequest object.
    - username: Username of the profile to be updated.

    Returns:
    - HttpResponse: Rendered template with updated profile data.

    Raises:
    - PermissionDenied: If the requesting user does not have permission to edit the profile.
    """
    profile = get_object_or_404(Profile, user__username=username)

    if request.user != profile.user:
        raise PermissionDenied("You don't have permission to edit this profile")

    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('accounts:profile_detail', username=profile.user.username)
        else:
            context = {
                'form': form,
                'form_errors': form.errors
            }
            return render(request, 'accounts/profile/update.html', context)

    form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile/update.html', {'form': form})
