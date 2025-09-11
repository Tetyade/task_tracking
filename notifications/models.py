from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.urls import reverse


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        MENTION = "mention", "Згадка"
        DUE_SOON = "due_soon", "Наближення дедлайну"
        SYSTEM = "system", "Системне"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="sent_notifications"
    )
    task = models.ForeignKey("tasks.Task", on_delete=models.CASCADE, null=True, blank=True)

    type = models.CharField(max_length=20, choices=NotificationType.choices)

    message = models.TextField()  # текст повідомлення, з посиланням на task
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_type_display()} → {self.recipient.username}"

    def get_absolute_url(self):
        if self.task:
            return reverse("tasks:task-detail", args=[self.task.pk])
        return "#"

class UserNotificationSetting(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mention_enabled = models.BooleanField(default=True)
    due_soon_enabled = models.BooleanField(default=True)
    system_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification settings for {self.user.username}"
