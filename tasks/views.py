from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from tasks import models
from tasks.forms import TaskForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class TaskListView(ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

class TaskDetailView(DetailView):
    model = models.Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'

class TaskCreateView(CreateView):
    model = models.Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')
