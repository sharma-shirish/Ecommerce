from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib import messages
from .forms import UserRegisterForm


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            return redirect('home')

    else:
        form = UserRegisterForm

    return render(request, 'register.html', {'form': form})


# Create your views here.
def registration(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print(f'In Post')
        if form.is_valid():
            print(f'Valid credentials')
            form.save()
            print(f'saved')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            messages.success(request, f'Account Created for {username}')

            print(f'Account Created for {username}')

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('shop')
        else:
            print(f'error')
            print(messages.get_messages(request))
    else:
        print(f'outside Post')
        form = UserRegisterForm

    return render(request, 'registration.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        messages.success(request, f' {username} Successfully Logged in')
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('shop')
        else:
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    # Redirect to a success page.
    return redirect('shop')



