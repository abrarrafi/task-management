from django.contrib import admin

# Register your models here.
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'user', 'task_name', 'start_date', 'end_date', 'status', 'tag')
