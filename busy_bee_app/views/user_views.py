from django.http import request
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F

from ..models import Profile,Task
from ..handle_messges import handle_response_message
from ..forms import RegisterForm,ProfileForm

def register_view(request):
    
    
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request,new_user)
            return redirect('home')


    context ={
        'form':form
    }
    return render(request,'registration/register.html',context)

class MyLoginView(SuccessMessageMixin, LoginView):
    template_name='registration/login.html'
    success_message = "Welcome back, %(username)s!, let's get Beesy"


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    tasks = Task.objects.filter(user=request.user)
    
    # for task in tasks.all():
    #     if task.is_completed:
    #         print(task.task_name)
    
    #     for logs in task.child_task_logs.all():
    #         print(logs.mini_task.mini_task_name)
        
    #     print('task name:', task.task_name,' ',' -num_logs',' ',task.child_task_logs.count())

    total_completed_task_logs = request.user.task_logs.all()

    total_completed_task_count = request.user.task_logs.count()

    on_time_logs = request.user.task_logs.filter(date_completed__lte=F('task__task_deadline')).count()

    if total_completed_task_count >0:
        efficiency_percentage = (on_time_logs/total_completed_task_count) * 100
    else:
        efficiency_percentage = 0


    context ={
        'profile':profile,
        'total_completed_task_logs':total_completed_task_logs,
        "total_completed_task_count":total_completed_task_count,
        'on_time_logs':on_time_logs
    }

    return render(request,'user/profile.html',context)

@login_required
def update_profile(request):
    profile = get_object_or_404(Profile, user = request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {
        'form':form
    }
    return render(request,'user/update_profile.html',context)

