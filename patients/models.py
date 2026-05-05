from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone = PhoneNumberField(blank=True, region='RU')
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"
        ordering = ["last_name", "first_name"]


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    phone = PhoneNumberField(blank=True, region='RU')
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.specialization})"

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        ordering = ["last_name", "first_name"]
