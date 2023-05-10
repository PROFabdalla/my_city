from django.db import models
from user_app.models import User


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
            "created_at": self.created_at,
        }
