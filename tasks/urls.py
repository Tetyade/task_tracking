from django.urls import path
from tasks import views
from comments.views import TaskDetailWithCommentsView, CommentDeleteView

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path("<int:pk>/", TaskDetailWithCommentsView.as_view(), name="task-detail"),
    path('create/', views.TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('<int:pk>/update-status/', views.TaskStatusUpdateView.as_view(), name='task-status-update'),

    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
    
]

app_name = 'tasks'