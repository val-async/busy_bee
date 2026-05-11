from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
# from datetime import timezone
from django.utils import timezone
from django.db.models import F

def validate_future_date(value):
    if value < timezone.now():
        raise ValidationError('silly bee, deadline cannot be in the past')

# Create your models here.
class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True,blank=True)
    #gamify levels, 15 tasks completed before deadline takes you to the next level
    # level = models.PositiveIntegerField(null=True,blank=True)

    @property
    def get_user_level(self):
        on_time_logs = self.user.task_logs.filter(date_completed__lte=F('task__task_deadline')).count()

        level = 1 + (on_time_logs//15)
        return level

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='tasks')
    task_name = models.CharField(max_length=150)
    task_deadline = models.DateTimeField(validators=[validate_future_date])
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=150,null=True,blank=True)
    is_completed = models.BooleanField(default=False)

    @property
    def listfy_notes(self):
        if len(self.notes) > 0 :
            note_list = self.notes.split()
        else:
            return ''
        if len(note_list) > 0:
            return note_list
        else: return ''

class MiniTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='mini_tasks')
    parent_task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='child_tasks')
    mini_task_name = models.CharField(max_length=150)
    mini_task_deadline = models.DateTimeField(validators=[validate_future_date])
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=150,null=True,blank=True)
    is_completed = models.BooleanField(default=False)

class TaskLogs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='task_logs')
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    date_completed = models.DateTimeField(auto_now_add=True)
    log_notes = models.TextField(max_length=250,blank=True,null=True)

    @property
    def was_on_time(self):
        return self.date_completed <= self.task.task_deadline
    
    @property
    def delay_duration(self):
        if self.was_on_time or not self.date_completed:
            return "On time"
        return self.date_completed - self.task.task_deadline

class MiniTaskLogs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='mini_task_logs')
    parent_task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='child_task_logs') 
    mini_task = models.ForeignKey(MiniTask,on_delete=models.CASCADE)
    date_completed = models.DateTimeField(auto_now_add=True)
    log_notes = models.TextField(max_length=250,blank=True,null=True)

    
    @property
    def was_on_time(self):
        return self.date_completed <= self.mini_task.mini_task_deadline
    
    @property
    def delay_duration(self):
        if self.was_on_time or not self.date_completed:
            return "On time"
        return self.date_completed - self.task.task_deadline


