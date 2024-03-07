from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import RegisterForm


User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already have account')
        return redirect('blog:post_list')

    form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
