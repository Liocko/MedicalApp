import io
import random

from django import forms
from PIL import Image, ImageDraw, ImageFont

AVATAR_COLOR_BLUE = '#6C8EBF'
AVATAR_COLOR_GREEN = '#82B366'
AVATAR_COLOR_ORANGE = '#D79B00'
AVATAR_COLOR_RED = '#AE4132'
AVATAR_COLOR_GRAY = '#647687'
AVATAR_COLOR_PURPLE = '#9673A6'

AVATAR_COLORS = [
    AVATAR_COLOR_BLUE,
    AVATAR_COLOR_GREEN,
    AVATAR_COLOR_ORANGE,
    AVATAR_COLOR_RED,
    AVATAR_COLOR_GRAY,
    AVATAR_COLOR_PURPLE,
]

AVATAR_SIZE = 200
AVATAR_FONT_SIZE = 80
AVATAR_TEXT_COLOR = (255, 255, 255)

FONT_PATHS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
]


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def generate_avatar(letter):
    color = random.choice(AVATAR_COLORS)
    bg_color = hex_to_rgb(color)

    img = Image.new('RGB', (AVATAR_SIZE, AVATAR_SIZE), color=bg_color)
    draw = ImageDraw.Draw(img)

    text = letter.upper()
    font = None
    for font_path in FONT_PATHS:
        try:
            font = ImageFont.truetype(font_path, AVATAR_FONT_SIZE)
            break
        except (IOError, OSError):
            continue

    if font is None:
        try:
            font = ImageFont.load_default(size=AVATAR_FONT_SIZE)
        except TypeError:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (AVATAR_SIZE - text_width) / 2 - bbox[0]
    y = (AVATAR_SIZE - text_height) / 2 - bbox[1]
    draw.text((x, y), text, fill=AVATAR_TEXT_COLOR, font=font)

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.read()


def normalize_phone(phone):
    """Validate and normalize phone to +7XXXXXXXXXX format."""
    if not phone:
        return phone
    if phone.startswith('8') and len(phone) == 11 and phone[1:].isdigit():
        return '+7' + phone[1:]
    if phone.startswith('+7') and len(phone) == 12 and phone[2:].isdigit():
        return phone
    raise forms.ValidationError(
        'Неверный формат номера телефона. Используйте 8XXXXXXXXXX или +7XXXXXXXXXX'
    )
