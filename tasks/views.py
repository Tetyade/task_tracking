from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from tasks import models
from tasks.forms import TaskForm, TaskFilterForm
from tasks.mixins import UserIsOwnerMixin
from django.db.models import F
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

class TaskListView(ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        # sort = self.request.GET.get("sort", "created_at")  
        # order = self.request.GET.get("order", "desc") 
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        sort = self.request.GET.get("sort")

        if sort == "due_date":
            queryset = queryset.order_by(F('due_date').asc(nulls_last=True))
        elif sort == "created_at":
            queryset = queryset.order_by('-created_at')
        elif sort == "priority":
            queryset = queryset.order_by('priority')
        else:
            queryset = queryset.order_by('-created_at')

        # allowed_fields = {
        #     "created_at": "created_at",
        #     "due_date": F("due_date").asc(nulls_last=True),
        #     "priority": "priority",
        # }

        # if sort in allowed_fields:
        #     if sort == "due_date":
        #         queryset = queryset.order_by(
        #             allowed_fields["due_date"] if order == "asc"
        #             else F("due_date").desc(nulls_last=True)
        #         )
        #     else:
        #         queryset = queryset.order_by(
        #             allowed_fields[sort] if order == "asc"
        #             else f"-{allowed_fields[sort]}"
        #         )

        if priority:
            queryset = queryset.filter(priority=priority)
        if status:
            queryset = queryset.filter(status=status)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        return context

class TaskDetailView(DetailView):
    model = models.Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.all().order_by('-created_at')  # новіші коментарі зверху

        # Тут додаємо властивість current_user для шаблону
        for comment in comments:
            comment.current_user = self.request.user

        context['comments'] = comments
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
class TaskStatusUpdateView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post (self, request, *args, **kwargs):
        task = self.get_object()
        new_status = request.POST.get('status')

        if new_status in dict(models.Task.STATUS_CHOICES):
            task.status = new_status
            task.save()

        return redirect("tasks:task-list")
        # return HttpResponseRedirect(reverse_lazy('tasks:task-list'))

    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(models.Task, pk=task_id)
    
class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = TaskForm
    template_name = 'tasks/task_update_form.html'
    def get_success_url(self):
        return reverse_lazy('tasks:task-detail', kwargs={'pk': self.object.pk})

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Task 
    success_url = reverse_lazy('tasks:task-list')
    template_name = 'tasks/task_confirm_delete.html'