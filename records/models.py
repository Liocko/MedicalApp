from django.db import models
from patients.models import Patient, Doctor


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="records")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="records")
    title = models.CharField(max_length=200)
    description = models.TextField()
    diagnosis = models.CharField(max_length=300, blank=True)
    appointment_time = models.DateTimeField(null=True, blank=True, verbose_name="Время записи")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.patient}"

    class Meta:
        verbose_name = "Медицинская запись"
        verbose_name_plural = "Медицинские записи"
        ordering = ["-created_at"]


class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="reports")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reports")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Отчёт: {self.title} — {self.patient}"

    class Meta:
        verbose_name = "Отчёт"
        verbose_name_plural = "Отчёты"
        ordering = ["-created_at"]
