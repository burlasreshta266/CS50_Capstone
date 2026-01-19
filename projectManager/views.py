from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm


@login_required
def index(request):
    return render(request, "projectManager/index.html")


def login(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('login')
        else:
            messages.error(request, "Invalid details")
            return render(request, "projectManager/login.html", {
            'form' : form
        })
    else:
        return render(request, "projectManager/login.html", {
            'form' : LoginForm()
        })


def register(request):
    if request.method=="POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User successfully registered! You can now login")
            return redirect('login')
        else:
            messages.error(request, "Invalid details")
            return render(request, "projectManager/register.html", {
            'form' : form
        })
    else:
        return render(request, "projectManager/register.html", {
            'form' : RegistrationForm()
        })