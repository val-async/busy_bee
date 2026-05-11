from django.shortcuts import render,redirect
from django.http import request

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('view_tasks')
    return render(request,'busy/home.html')