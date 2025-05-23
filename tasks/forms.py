from django import forms
from .models import Task
from django.utils import timezone

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'start_date', 'start_time', 'end_date', 'end_time', 'status', 'tag']
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        now = timezone.localtime()
        time_now = now.time().replace(second=0, microsecond=0)

        if not self.instance.pk:  # Only set defaults on new task
            self.fields['start_date'].initial = now.date()
            self.fields['start_time'].initial = time_now
            self.fields['end_date'].initial = now.date()
            self.fields['end_time'].initial = time_now
