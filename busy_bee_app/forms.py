from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
# from django.forms import forms


from .models import Profile,Task,TaskLogs,MiniTask,MiniTaskLogs

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='confirm password')
  
    class Meta:
        model = User
        fields = ['username','password','email']

    field_order = ['username', 'email','password', 'password_confirm']


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        
        return cleaned_data
    
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name','task_deadline','notes']

        # labels = {}
        widgets = {
            'task_name': forms.TextInput(attrs={'placeholder':'e.g Finish Editing, Make a video For..'}),
            'task_deadline': forms.DateInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 6, 'placeholder': '(Optional)Task notes...'}),
        }

class MiniTaskForm(forms.ModelForm):
    class Meta:
        model = MiniTask
        fields = ['mini_task_name','mini_task_deadline','notes']

        widgets = {
            'mini_task_name': forms.TextInput(attrs={'placeholder':'task chunks'}),
            'mini_task_deadline': forms.DateInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Brief notes...'}),

        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth']

        widgets={
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if we are updating an existing record (not creating a new one)
        if self.instance and self.instance.date_of_birth is not None:
            self.fields['date_of_birth'].disabled = True

# class TaskLogs()
# class TaskLogs(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name='task_logs')
#     task = models.ForeignKey(Task,on_delete=models.CASCADE)
#     date_completed = models.DateTimeField(auto_now_add=True)
#     log_notes = models.TextField(max_length=250,blank=True,null=True)

# class MiniTaskLogs(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name='mini_task_logs')
#     parent_task_log = models.ForeignKey(TaskLogs,on_delete=models.CASCADE,related_name='child_task_logs') 
#     mini_task = models.ForeignKey(MiniTask,on_delete=models.CASCADE)
#     date_completed = models.DateTimeField(auto_now_add=True)
#     log_notes = models.TextField(max_length=250,blank=True,null=True)