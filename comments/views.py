from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, View
from .models import Comment
from .forms import CommentForm
from tasks.models import Task
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from notifications.utils import process_mentions
from comments.models import CommentLike
from django.contrib.auth.decorators import login_required

class TaskDetailWithCommentsView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all().order_by("-created_at")
        # context["comments"] = self.object.comments.select_related("author")
        context["form"] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = self.object

            # викликаємо утиліту
            comment.content = process_mentions(comment, request.user)

            comment.save()
            return redirect("tasks:task-detail", pk=self.object.pk)

        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)

class CommentDeleteView(UserPassesTestMixin, View):

    def test_func(self):
        # admin or staff only
        return self.request.user.is_staff or self.request.user.is_superuser
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        task_pk = comment.task.pk
        comment.delete()
        return redirect("tasks:task-detail", pk=task_pk)
    
@login_required
def toggle_like(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like.delete()  # якщо лайк вже був — видаляємо (toggle)
    return redirect("tasks:task-detail", pk=comment.task.pk)
