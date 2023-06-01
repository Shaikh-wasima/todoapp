from django.contrib import messages
from .models import CustomUser, Task
from .forms import CustomUserCreationForm, LoginForm, TaskForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def task_list(request):
    if request.user.is_superuser:
        tasks = Task.objects.filter(created_by=request.user) | Task.objects.filter(assigned_to=request.user)
    else:
        tasks = Task.objects.filter(assigned_to=request.user) | Task.objects.filter(created_by=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_create.html', {'form': form})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.user.is_superuser or task.created_by == request.user:
        form = TaskForm(request.POST or None, instance=task)
    else:
        form = TaskForm(request.POST or None, instance=task, initial={'completed': task.completed})
        form.fields['title'].disabled = True
        form.fields['description'].disabled = True
        form.fields['assigned_to'].disabled = True    

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('task_list')

    return render(request, 'task_update.html', {'form': form, 'task': task})


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if not request.user.is_superuser and task.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task, 'admin': request.user.is_superuser})

def logout_view(request):
    logout(request)
    return redirect('login')