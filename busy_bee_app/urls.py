from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.home,name='home'),
    path('view_tasks/',views.view_tasks,name='view_tasks'),
    path('create_task/',views.create_task,name='create_task'),
    path('add_mini_task/<int:task_id>/',views.add_mini_task,name='add_mini_task'),
    path('remove_mini_task/<int:mini_task_id>/',views.remove_mini_task,name='remove_mini_task'),
    path('delete_task/<int:task_id>/',views.delete_task,name="delete_task"),
    path('register/',views.register_view,name='register'),
    path('login/',views.MyLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',views.profile_view,name='profile'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('log_mini_task/<int:task_id>/<int:mini_task_id>/',views.log_mini_task,name='log_mini_task'),
    path('log_task/<int:task_id>/',views.log_task,name='log_task')
    
]
