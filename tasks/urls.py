from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', TaskDashboardView.as_view(), name='task-dashboard'),
    path('task-list/', TaskListView.as_view(), name='task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/events/', views.events_api, name='events_api'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='task-edit'),
]
