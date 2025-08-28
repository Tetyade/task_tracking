from django.shortcuts import render, get_object_or_404, redirect
# accounts/views.py
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, UpdateView
from .models import CustomUser
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Task

class UserRegisterView(FormView):
    template_name = "auth_system/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = "auth_system/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy(self.get_redirect_url() or "tasks:task-list")

class MyProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "auth_system/profile.html"
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        context["task_stats"] = Task.objects.filter(creator=user).aggregate(
            total=Count("id"),
            completed=Count("id", filter=Q(status="done")),
            not_completed=Count("id", filter=Q(status="todo")),
            urgent=Count("id", filter=Q(priority=1)),
        )
        return context

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "auth_system/profile.html"
    context_object_name = "user_profile"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

class MyProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "auth_system/profile_update.html"
    fields = ["username", "email", "first_name", "last_name"]

    def get_object(self, queryset=None):
        # завжди повертаємо саме поточного користувача
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy("auth:my-profile")
# class ProfileUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
#     model = CustomUser
#     template_name = "auth_system/profile_update.html"
#     fields = ["username", "email", "first_name", "last_name"]
#     slug_field = "uuid"
#     slug_url_kwarg = "uuid"
    
#     def get_success_url(self):
#         return reverse_lazy("auth:profile", kwargs={"uuid": self.object.uuid})

