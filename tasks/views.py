from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm

from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView
from .models import Task

from django.utils import timezone
from django.views.generic import TemplateView
from django.db.models import Q
from .models import Task

class TaskDashboardView(TemplateView):
    template_name = 'tasks/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        user = self.request.user

        # Tasks for today that are not completed
        context['tasks_today'] = Task.objects.filter(
            user=user,
            start_date=today
        ).exclude(status='Completed')

        # Tasks not today (past or future) that are not completed
        context['tasks_others'] = Task.objects.filter(
            user=user
        ).exclude(start_date=today).exclude(status='Completed')

        return context



class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)

        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        status = self.request.GET.get('status')

        if from_date:
            queryset = queryset.filter(start_date__gte=from_date)
        else:
            from_date = timezone.now().date()
            queryset = queryset.filter(start_date__gte=from_date)

        if to_date:
            queryset = queryset.filter(end_date__lte=to_date)

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date().isoformat()
        return context


# class TaskCreateView(LoginRequiredMixin, CreateView):
#     model = Task
#     form_class = TaskForm
#     template_name = 'tasks/task_form.html'
#     success_url = reverse_lazy('task-list')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

    def get_initial(self):
        initial = super().get_initial()
        start_date = self.request.GET.get('start_date')
        if start_date:
            initial['start_date'] = start_date
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-dashboard')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-dashboard')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Task
from datetime import datetime

@login_required
def calendar_view(request):
    return render(request, 'tasks/calendar.html')

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def events_api(request):
    tasks = Task.objects.filter(user=request.user)
    events = []
    for t in tasks:
        start_datetime = f"{t.start_date}T{t.start_time}"
        end_datetime = f"{t.end_date}T{t.end_time}"

        events.append({
            'id': t.id,  # keep using the DB ID if your form/edit view uses it
            'title': t.task_name,
            'start': start_datetime,
            'end': end_datetime,
            'allDay': False,
            'url': f"/tasks/{t.pk}/edit/"  # URL that points to the edit form
        })
    return JsonResponse(events, safe=False)




