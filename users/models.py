import random
import io

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.files.base import ContentFile

from PIL import Image, ImageDraw, ImageFont


AVATAR_COLORS = ['#6C8EBF', '#82B366', '#D79B00', '#AE4132', '#647687', '#9673A6']


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def generate_avatar(letter):
    size = 200
    color = random.choice(AVATAR_COLORS)
    bg_color = hex_to_rgb(color)

    img = Image.new('RGB', (size, size), color=bg_color)
    draw = ImageDraw.Draw(img)

    text = letter.upper()
    font = None

    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    ]

    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, 80)
            break
        except (IOError, OSError):
            continue

    if font is None:
        try:
            font = ImageFont.load_default(size=80)
        except TypeError:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) / 2 - bbox[0]
    y = (size - text_height) / 2 - bbox[1]

    draw.text((x, y), text, fill=(255, 255, 255), font=font)

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.read()


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=12, blank=True)
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    favorites = models.ManyToManyField(
        'projects.Project',
        blank=True,
        related_name='interested_users'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            first_letter = self.name[0] if self.name else 'U'
            avatar_data = generate_avatar(first_letter)
            filename = f'avatar_{self.email.split("@")[0]}.png'
            self.avatar.save(filename, ContentFile(avatar_data), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname} <{self.email}>'
