from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import RegistrationForm, LoginForm, ProjectForm, TechnologyForm


def index(request):
    return render(request, "projectManager/index.html")


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user 
            project.save()
            form.save_m2m()
            messages.success(request, "Project created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProjectForm()

    tech_form = TechnologyForm()
    return render(request, "projectManager/create_project.html", {
        'form': form,
        'tech_form': tech_form,
    })


def project(request, id):
    project = Project.objects.all().get(id=id)
    technologies = project.technologies.all()
    return render(request, "projectManager/project.html", {
        "project" : project,
        "technologies" : technologies,
    })


@login_required
def add_technology(request):
    if request.method == "POST":
        form = TechnologyForm(request.POST)
        if form.is_valid():
            tech = form.save()
            return JsonResponse({'success': True, 'id': tech.id, 'name': tech.name})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def delete_project(request, id):
    project = Project.objects.all().get(id=id)
    if request.user!=project.creator:
        messages.error(request, "You are not the project creator. Only the creator of the project can delete it.")
        redirect("project", id=project.id)
    else:
        Project.objects.delete(project)
        redirect("home")


@login_required
def home(request):
    projects = request.user.projects.all()
    return render(request, "projectManager/home.html", {
        'projects' : projects,
    })


def logout(request):
    auth.logout(request, request.user)
    return redirect('index')


def login(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('home')
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