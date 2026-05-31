from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models

from .managers import UserManager
from .utils import generate_avatar

USER_NAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=USER_PHONE_MAX_LENGTH, blank=True)
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=USER_ABOUT_MAX_LENGTH, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    favorites = models.ManyToManyField(
        'projects.Project',
        blank=True,
        related_name='interested_users',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} {self.surname} <{self.email}>'

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            first_letter = self.name[0] if self.name else 'U'
            avatar_data = generate_avatar(first_letter)
            filename = f'avatar_{self.email.split("@")[0]}.png'
            self.avatar.save(filename, ContentFile(avatar_data), save=False)
        super().save(*args, **kwargs)
