from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Subquery
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Patient, Doctor
from .forms import PatientForm, DoctorForm


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        from records.models import MedicalRecord
        last = MedicalRecord.objects.filter(patient=OuterRef('pk')).order_by('-created_at')
        base_qs = Patient.objects.annotate(
            last_visit=Subquery(last.values('created_at')[:1]),
            last_doctor=Subquery(last.values('doctor__last_name')[:1]),
        ).order_by('last_name', 'first_name')
        q = self.request.GET.get('q', '').strip().lower()
        if q:
            pks = [p.pk for p in base_qs
                   if q in p.last_name.lower() or q in p.first_name.lower()
                   or q in str(p.phone or '').lower()]
            return base_qs.filter(pk__in=pks)
        return base_qs


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p = self.object
        ctx['records'] = p.records.select_related('doctor').order_by('-created_at')
        ctx['patient_info'] = [
            ('Дата рождения', p.date_of_birth.strftime('%d.%m.%Y'), True),
            ('Телефон', str(p.phone) if p.phone else '—', True),
            ('Email', p.email or '—', False),
            ('Адрес', p.address or '—', False),
        ]
        return ctx


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/form.html'
    success_url = reverse_lazy('patients:list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Добавить пациента'
        return ctx


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/form.html'
    success_url = reverse_lazy('patients:list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Редактировать: {self.object}'
        return ctx


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patients/confirm_delete.html'
    success_url = reverse_lazy('patients:list')


class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'patients/doctor_list.html'
    context_object_name = 'doctors'


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'patients/doctor_form.html'
    success_url = reverse_lazy('patients:doctor_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Добавить врача'
        return ctx


class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'patients/doctor_form.html'
    success_url = reverse_lazy('patients:doctor_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Редактировать: {self.object}'
        return ctx


class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'patients/doctor_confirm_delete.html'
    success_url = reverse_lazy('patients:doctor_list')
