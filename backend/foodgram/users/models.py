from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authors",
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.author.username} – {self.follower.username}"
