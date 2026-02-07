from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    class Type(models.TextChoices):
        FOLLOW = 'follow', 'Follow'
        POST = 'post', 'Post'
        COMMENT = 'comment', 'Comment'
        LIKE = 'like', 'Like'

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
    )

    type = models.CharField(
        max_length=20,
        choices=Type.choices,
    )

    # generic target (post / comment / relation / like / ...)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['to_user', 'is_read']),
        ]

    def __str__(self):
        return f"{self.type} → {self.to_user}"

    def get_read_url(self):
        return reverse('notifications:notification-read', args=[self.pk])

    def get_delete_url(self):
        return reverse('notifications:notification-delete', args=[self.pk])
