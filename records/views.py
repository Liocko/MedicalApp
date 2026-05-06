from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from patients.models import Doctor
from .models import MedicalRecord
from .forms import MedicalRecordForm


class RecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'records/list.html'
    context_object_name = 'records'

    def get_queryset(self):
        qs = MedicalRecord.objects.select_related('patient', 'doctor')

        # SQL-фильтры (работают в SQLite корректно)
        if doctor_id := self.request.GET.get('doctor'):
            qs = qs.filter(doctor_id=doctor_id)
        if date_from := self.request.GET.get('date_from'):
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to := self.request.GET.get('date_to'):
            qs = qs.filter(created_at__date__lte=date_to)

        # Python-фильтрация для кириллицы: SQLite не поддерживает
        # case-insensitive LIKE для не-ASCII символов
        patient_q = self.request.GET.get('patient', '').strip().lower()
        diagnosis_q = self.request.GET.get('diagnosis', '').strip().lower()

        if patient_q or diagnosis_q:
            pks = []
            for r in qs:
                if patient_q and patient_q not in r.patient.last_name.lower() \
                        and patient_q not in r.patient.first_name.lower():
                    continue
                if diagnosis_q and diagnosis_q not in (r.diagnosis or '').lower():
                    continue
                pks.append(r.pk)
            qs = MedicalRecord.objects.select_related('patient', 'doctor').filter(pk__in=pks)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['doctors'] = Doctor.objects.all()
        ctx['f'] = self.request.GET
        return ctx


class RecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'records/detail.html'
    context_object_name = 'record'


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        rec = self.object
        messages.success(
            self.request,
            f'{rec.patient}|{rec.title}|{rec.doctor}',
            extra_tags='ws_notification',
        )
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Новая запись'
        return ctx


class RecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Редактировать запись'
        return ctx


class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicalRecord
    template_name = 'records/confirm_delete.html'
    success_url = reverse_lazy('records:list')


class ScheduleView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'records/schedule.html'
    context_object_name = 'records'

    def get_queryset(self):
        return MedicalRecord.objects.select_related('patient', 'doctor').order_by(
            'doctor__last_name', '-created_at'
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()

        # Загрузка врачей: общее число записей каждого
        doctors = Doctor.objects.annotate(
            total=Count('records'),
        ).filter(total__gt=0).order_by('last_name')

        # Записи сегодня (по appointment_time если задан, иначе по created_at)
        today_records = MedicalRecord.objects.select_related(
            'patient', 'doctor'
        ).filter(
            Q(appointment_time__date=today) |
            Q(appointment_time__isnull=True, created_at__date=today)
        ).order_by('-appointment_time', '-created_at')

        ctx['doctors'] = doctors
        ctx['today'] = today
        ctx['today_records'] = today_records
        return ctx
