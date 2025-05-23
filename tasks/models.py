from django.db import models
from django.contrib.auth.models import User
import re

class Task(models.Model):
    task_id = models.CharField(max_length=10, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('In_progress', 'In_progress'),
        ('Completed', 'Completed'),
        ('Upcomming', 'Upcomming'),
    ])
    tag = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'task_id')
        ordering = ['-start_date', '-start_time']

    def save(self, *args, **kwargs):
        if not self.task_id:
            last_task = Task.objects.filter(user=self.user).order_by('-task_id').first()
            if last_task:
                match = re.search(r'TSK-(\d+)', last_task.task_id)
                next_id = int(match.group(1)) + 1 if match else 1
            else:
                next_id = 1
            self.task_id = f'TSK-{next_id:06d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task_id} - {self.task_name}"
