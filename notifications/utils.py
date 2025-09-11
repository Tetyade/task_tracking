import re
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.html import escape
from .models import Notification

User = get_user_model()

def process_mentions(comment, actor):
    """
    Безпечна обробка згадок у коментарі:
    - замінює @username на HTML-посилання
    - створює нотифікації для згаданих користувачів
    """
    pattern = r"@([\w-]+)"

    def replace_mention(match):
        username = match.group(1)
        try:
            mentioned_user = User.objects.get(username=username)
            Notification.objects.create(
                recipient=mentioned_user,
                actor=actor,
                task=comment.task,
                message=f"{actor.username} згадав вас у цьому завданні"
            )
            profile_url = reverse_lazy("profile-detail", args=[mentioned_user.uuid])
            return f'<a href="{profile_url}">@{escape(username)}</a>'
        except User.DoesNotExist:
            return f"@{escape(username)}"

    # Екрануємо весь текст, а згадки перетворюємо на HTML
    safe_content = escape(comment.content)
    safe_content = re.sub(pattern, replace_mention, safe_content)
    return safe_content
