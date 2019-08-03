from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm


# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data['username']
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        user_form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form
    })
