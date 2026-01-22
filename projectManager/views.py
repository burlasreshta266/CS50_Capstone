from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import RegistrationForm, LoginForm, ProjectForm, TechnologyForm, TaskForm


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
    tasks = project.tasks.all()
    task_form = TaskForm()
    return render(request, "projectManager/project.html", {
        "project" : project,
        "technologies" : technologies,
        "tasks" : tasks,
        "task_form": task_form,
    })


@login_required
def edit_project(request, id):
    project = Project.objects.get(id=id)

    if request.user != project.creator:
        messages.error(request, "You are not authorized to edit this project.")
        return redirect('project', id=id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect('project', id=id)
    else:
        form = ProjectForm(instance=project)

    tech_form = TechnologyForm()

    return render(request, "projectManager/edit_project.html", {
        "form": form,
        "tech_form": tech_form,
        "project": project
    })


@require_POST
@login_required
def mark_project_complete(request, id):
    project = Project.objects.get(id=id)
    
    if request.user != project.creator:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    project.status = 'completed'
    project.save()
    
    return JsonResponse({
        'success': True,
        'status': project.status
    })


@require_POST
def mark_task_complete(request, id):
    task = Task.objects.all().get(id=id)
    task.status = 'completed'
    task.save()
    return JsonResponse({
        'curr_status' : task.status
    })


@require_POST
@login_required
def add_task(request, id):
    project = Project.objects.get(id=id)
    form = TaskForm(request.POST)

    if form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()
        messages.success(request, "Task added successfully!")
    else:
        messages.error(request, "Error adding task. Please check the date format.")
    
    return redirect('project', id=id)


@require_POST
def edit_task(request, id):
    task = Task.objects.get(id=id)
    form = TaskForm(request.POST, instance=task)
    
    if form.is_valid():
        task = form.save()
        return JsonResponse({
            'success': True,
            'title': task.title,
            'deadline': task.deadline.strftime("%b. %d, %Y, %I:%M %p") 
        })
    return JsonResponse({'success': False, 'errors': form.errors})


def delete_task(request, id):
    task = Task.objects.get(id=id)
    p_id = task.project.id
    task.delete()
    return redirect('project', id=p_id)


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
        project.delete()
        return redirect("home")


@login_required
def home(request):
    projects = request.user.projects.all()
    return render(request, "projectManager/home.html", {
        'projects' : projects,
    })


def logout(request):
    auth.logout(request)
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