from django.http import HttpResponse, JsonResponse
from .models import Project, Task
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateNewTask, CreateNewProject
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    if str(request.user)=='AnonymousUser':
        title = 'Hello'
    else:
        user = str(request.user)
        title = 'Hello '+user

    return render(request, 'index.html', {
        'title': title
    })

@login_required
def projects(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects/projects.html', {
        'projects': projects
    })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
            'form': CreateNewTask()
        })
    else:
        try:
            form = CreateNewTask(request.POST)
            new_task = form.save()
            new_task.user = request.user
            new_task = form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/create_task.html', {
                'form': CreateNewTask(),
                'error': 'Please provide value data'
            })

@login_required
def update_task(request, id):
    if request.method == 'GET':
        task = get_object_or_404(Task, id = id)
        form = CreateNewTask(instance=task)
        return render(request, 'tasks/update_task.html', {
            'task': task,
            'form': form,
        })
    else:
        try:
            task= get_object_or_404(Task, id = id)
            form = CreateNewTask(request.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/update_task.html', {
            'task': task,
            'form': form,
            'error' : 'Error updating task'
        })

@login_required
def complete_task(request, id):
    task = get_object_or_404(Task, id= id)
    if request.method == 'POST':
        task.datecompleted= timezone.now()
        task.done = True
        task.save()
        return redirect('tasks')

@login_required  
def delete_task(request, id):
    task = get_object_or_404(Task, id= id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject()
        })
    else:
        form = CreateNewProject(request.POST)
        new_project = form.save()
        new_project.user = request.user
        new_project.save()
        return redirect('projects')

@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=id)
    return render(request, 'projects/detail.html', {
        'project': project,
        'tasks': tasks
    })

@login_required
def delete_project(request, id):
    project = get_object_or_404(Project, id= id)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password dont match'
        })

@login_required 
def signout(request):
    #<link rel="stylesheet" href="{% static 'styles/main.css' %}">
    logout(request)
    return redirect('index')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('projects')
