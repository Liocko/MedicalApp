from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from patients.models import Patient, Doctor
from records.models import MedicalRecord
from .forms import UserForm, ProfileForm
from .models import UserProfile


@login_required
def index(request):
    from django.utils import timezone
    today = timezone.localdate()
    context = {
        'patient_count': Patient.objects.count(),
        'doctor_count': Doctor.objects.count(),
        'record_count': MedicalRecord.objects.count(),
        'today_count': MedicalRecord.objects.filter(created_at__date=today).count(),
        'recent_records': MedicalRecord.objects.select_related('patient', 'doctor').order_by('-created_at')[:6],
    }
    return render(request, 'core/index.html', context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return render(request, 'core/profile.html', {
            'user_form': UserForm(instance=request.user),
            'profile_form': ProfileForm(instance=profile),
        })

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлён.')
            return redirect('profile')
        return render(request, 'core/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })
