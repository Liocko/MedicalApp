from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Patient, Doctor
from .forms import PatientForm, DoctorForm


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/list.html'
    context_object_name = 'patients'


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['records'] = self.object.records.select_related('doctor').order_by('-created_at')
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
