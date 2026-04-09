from django.shortcuts import render,redirect,get_object_or_404
from django.http import request
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import Task,MiniTask,TaskLogs,MiniTaskLogs
from ..forms import TaskForm,MiniTaskForm
from ..handle_messges import handle_response_message

@login_required
def view_tasks(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'tasks':tasks
    }
    return render(request,'task/view_task.html',context)

@login_required
def create_task(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return handle_response_message(request,'successfully created')
    context = {
        'form':form
    }
    return render(request,'task/partial/create_task.html',context)

def edit_task(request):
    pass

def delete_task(request,task_id):
    task = get_object_or_404(Task,id=task_id)
    if request.method == 'POST':
        task.delete()
        return handle_response_message(request,'naughty bee ...👀 ')
    context ={
        'task':task
    }
    return render(request,'task/partial/delete_task.html',context)

#mini task
@login_required
def add_mini_task(request, task_id):
    task = get_object_or_404(Task,id=task_id)
    form = MiniTaskForm()
    
    if request.method == 'POST':
        form = MiniTaskForm(request.POST)
        if form.is_valid():
            new_mini_task = form.save(commit=False)
            new_mini_task.parent_task = task
            new_mini_task.user = request.user
            new_mini_task.save()
            return handle_response_message(request,"successful")


    context = {
        'task':task,
        'form':form,
        'task_id':task_id
    }

    return render(request,'task/partial/add_mini_task.html',context)

def edit_mini_task(request,task_id):
    pass

@login_required
def remove_mini_task(request,mini_task_id):
    mini_task = get_object_or_404(MiniTask,id=mini_task_id)
    if request.method == 'POST':
        mini_task.delete()
        return handle_response_message(request,'not so busy afterall ')
    
    context={
        'mini_task':mini_task
    }
    return render(request, 'task/partial/remove_mini_task.html',context)

@login_required
def log_task(request, task_id):

    task = get_object_or_404(Task, user=request.user,id=task_id)

    if request.method == 'POST':
        new_log = TaskLogs.objects.create(
            user = request.user,
            task = task,
            log_notes = task.notes
        )
        task.is_completed = True
        task.save()
        handle_response_message(request,'Task completed congratulations')
        return redirect('view_tasks')
    
    context = {
        'task':task
    }
    
    return render(request,'task/log_task.html',context)

@login_required
def log_mini_task(request,task_id, mini_task_id):
    
    task = get_object_or_404(Task, user=request.user,id=task_id)
    mini_task = get_object_or_404(MiniTask, user=request.user,id=mini_task_id)

    if request.method == 'POST':
        print('valid')
        try:
            new_mini_log = MiniTaskLogs.objects.create(
                user = request.user,
                parent_task = task,
                mini_task = mini_task,
                log_notes = mini_task.notes
            )
            mini_task.is_completed = True
            mini_task.save()
        except Exception as e:
            print(f'Error: {e}') 
        handle_response_message(request, 'keeping beeeessyyyy')
        return redirect('view_tasks')
    

