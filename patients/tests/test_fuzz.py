"""
Фаззинг-тесты для пациентов, врачей и медицинских записей.
Используют hypothesis для генерации случайных входных данных
и проверяют, что API не падает с 500 на произвольных входных данных.
"""
import json
import datetime
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase
from django.contrib.auth.models import User
from patients.models import Patient, Doctor


printable_text = st.text(
    alphabet=st.characters(whitelist_categories=('L', 'N', 'Zs')),
    min_size=1,
    max_size=100,
)

safe_text = st.text(
    alphabet=st.characters(whitelist_categories=('L', 'N', 'Zs')),
    min_size=0,
    max_size=300,
)


class PatientAPIFuzzTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('fuzz_patient_user', password='testpass123')

    def setUp(self):
        from django.test import Client
        self.client = Client()
        self.client.force_login(self.user)

    @given(
        first_name=printable_text,
        last_name=printable_text,
        date_of_birth=st.dates(
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date(2020, 12, 31),
        ),
        email=st.one_of(st.just(''), st.emails()),
        address=safe_text,
    )
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_create_patient_fuzz(self, first_name, last_name, date_of_birth, email, address):
        """API не должен возвращать 500 на произвольных (но типизированных) данных."""
        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': str(date_of_birth),
            'email': email,
            'address': address,
        }
        response = self.client.post(
            '/api/v1/patients/',
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertNotEqual(response.status_code, 500,
                            f"500 при данных: {payload}")

    @given(search_term=st.text(max_size=200))
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_search_patients_fuzz(self, search_term):
        """Поиск не должен падать ни на каком поисковом запросе."""
        response = self.client.get('/api/v1/patients/', {'search': search_term})
        self.assertIn(response.status_code, [200, 400],
                      f"Неожиданный статус {response.status_code} при поиске: {search_term!r}")


class DoctorAPIFuzzTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('fuzz_doctor_user', password='testpass123')

    def setUp(self):
        from django.test import Client
        self.client = Client()
        self.client.force_login(self.user)

    @given(
        first_name=printable_text,
        last_name=printable_text,
        specialization=printable_text,
        email=st.one_of(st.just(''), st.emails()),
    )
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_create_doctor_fuzz(self, first_name, last_name, specialization, email):
        """API создания врача не должен возвращать 500 на случайных данных."""
        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'specialization': specialization,
            'email': email,
        }
        response = self.client.post(
            '/api/v1/doctors/',
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertNotEqual(response.status_code, 500,
                            f"500 при данных: {payload}")


class MedicalRecordAPIFuzzTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('fuzz_record_user', password='testpass123')
        cls.patient = Patient.objects.create(
            first_name='Иван', last_name='Тестов',
            date_of_birth=datetime.date(1990, 1, 1),
        )
        cls.doctor = Doctor.objects.create(
            first_name='Врач', last_name='Тестов', specialization='Терапевт',
        )

    def setUp(self):
        from django.test import Client
        self.client = Client()
        self.client.force_login(self.user)

    @given(
        title=printable_text,
        description=safe_text,
        diagnosis=safe_text,
    )
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    def test_create_record_fuzz(self, title, description, diagnosis):
        """API создания записи не падает на случайных текстах."""
        payload = {
            'patient': self.patient.pk,
            'doctor': self.doctor.pk,
            'title': title,
            'description': description,
            'diagnosis': diagnosis,
        }
        response = self.client.post(
            '/api/v1/records/',
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertNotEqual(response.status_code, 500,
                            f"500 при данных: {payload}")

    @given(
        search_term=st.text(max_size=200),
        ordering=st.sampled_from(
            ['created_at', '-created_at', 'title', '-title', 'invalid_field', '']
        ),
    )
    @settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow])
    def test_list_records_fuzz(self, search_term, ordering):
        """Листинг записей не падает на произвольных query-параметрах."""
        response = self.client.get('/api/v1/records/', {
            'search': search_term,
            'ordering': ordering,
        })
        self.assertIn(response.status_code, [200, 400])
