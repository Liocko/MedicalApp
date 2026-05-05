from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import MedicalRecord
from .forms import MedicalRecordForm


class RecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'records/list.html'
    context_object_name = 'records'
    queryset = MedicalRecord.objects.select_related('patient', 'doctor')


class RecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'records/detail.html'
    context_object_name = 'record'


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:list')

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
