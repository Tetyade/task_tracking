from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path("comment/<int:comment_id>/like/", views.toggle_like, name="comment-like"),

]