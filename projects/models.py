from django.conf import settings
from django.db import models

PROJECT_NAME_MAX_LENGTH = 200
PROJECT_STATUS_MAX_LENGTH = 6
PROJECT_STATUS_OPEN = 'open'
PROJECT_STATUS_CLOSED = 'closed'


class Project(models.Model):
    STATUS_CHOICES = [
        (PROJECT_STATUS_OPEN, 'Open'),
        (PROJECT_STATUS_CLOSED, 'Closed'),
    ]

    name = models.CharField(max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=PROJECT_STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
