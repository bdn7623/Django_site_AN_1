from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .models import ActivationToken
from .utils import send_activation_email

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already have account')
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


def activate_account_view(request, username, token):
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
        return redirect('blog:post_list')

    messages.error(request, 'Token expired')
    return redirect('blog:post_list')


def login_view(request):
    
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
