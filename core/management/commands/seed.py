import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from patients.models import Patient, Doctor
from records.models import MedicalRecord, Report

LAST_NAMES = [
    "Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев",
    "Петров", "Соколов", "Михайлов", "Новиков", "Фёдоров",
    "Морозов", "Волков", "Алексеев", "Лебедев", "Семёнов",
    "Егоров", "Павлов", "Козлов", "Степанов", "Николаев",
    "Орлов", "Андреев", "Макаров", "Никитин", "Захаров",
    "Зайцев", "Соловьёв", "Борисов", "Яковлев", "Григорьев",
]

FEMALE_LAST_NAMES = [name + "а" for name in LAST_NAMES]

MALE_FIRST_NAMES = [
    "Александр", "Дмитрий", "Максим", "Сергей", "Андрей",
    "Алексей", "Артём", "Илья", "Кирилл", "Михаил",
    "Никита", "Роман", "Егор", "Иван", "Владимир",
]

FEMALE_FIRST_NAMES = [
    "Анна", "Мария", "Елена", "Ольга", "Татьяна",
    "Наталья", "Ирина", "Екатерина", "Юлия", "Светлана",
    "Виктория", "Дарья", "Ксения", "Полина", "Алина",
]

SPECIALIZATIONS = [
    "Терапевт", "Хирург", "Кардиолог", "Невролог", "Офтальмолог",
    "Дерматолог", "Эндокринолог", "Гастроэнтеролог", "Ортопед", "Педиатр",
]

DIAGNOSES = [
    "Гипертоническая болезнь II ст.", "ОРВИ", "Бронхит острый",
    "Остеохондроз поясничного отдела", "Сахарный диабет 2 типа",
    "Гастрит хронический", "Пневмония", "Мигрень", "Анемия",
    "Артериальная гипотензия", "Варикозная болезнь нижних конечностей",
    "Катаракта", "Отит средний", "Ринит аллергический", "Тревожное расстройство",
]

RECORD_TITLES = [
    "Первичный осмотр", "Повторный осмотр", "Плановый осмотр",
    "Консультация", "Контрольный осмотр", "Осмотр после лечения",
    "Диспансерное наблюдение", "Профилактический осмотр",
    "Осмотр по направлению", "Внеплановый осмотр",
]

DESCRIPTIONS = [
    "Пациент жалуется на головные боли, слабость, повышение АД до 160/100 мм рт.ст. "
    "Назначена антигипертензивная терапия. Рекомендован контроль АД.",

    "Жалобы на кашель, насморк, повышение температуры до 37.8°C. "
    "Назначена симптоматическая терапия. Рекомендован постельный режим.",

    "Пациент предъявляет жалобы на боли в поясничной области при движении. "
    "Назначена физиотерапия, НПВС. Рекомендовано ограничение физической нагрузки.",

    "Жалобы на периодические боли в эпигастральной области, изжогу. "
    "Назначена диета №1, ингибиторы протонной помпы. Рекомендована ЭГДС.",

    "Пациент жалуется на учащённое сердцебиение, одышку при нагрузке. "
    "ЭКГ — синусовая тахикардия. Назначено дополнительное обследование.",

    "Жалобы на снижение остроты зрения, дискомфорт при чтении. "
    "Выявлена миопия средней степени. Подобраны очки, рекомендован контроль.",

    "Плановый осмотр в рамках диспансерного наблюдения. Состояние стабильное. "
    "Терапия продолжается в прежнем объёме.",

    "Жалобы на зуд кожных покровов, высыпания на предплечьях. "
    "Назначены антигистаминные препараты, местная терапия.",
]

PHONES = [
    "+79161234567", "+79031112233", "+79851239876", "+79267778899",
    "+79104445566", "+79253334455", "+79876665544", "+79512223344",
]


def random_date(start_year=1950, end_year=2005):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))


class Command(BaseCommand):
    help = "Заполняет БД тестовыми данными"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Очистить данные перед заполнением")

    def handle(self, *args, **options):
        if options["clear"]:
            MedicalRecord.objects.all().delete()
            Report.objects.all().delete()
            Patient.objects.all().delete()
            Doctor.objects.all().delete()
            self.stdout.write("Данные очищены.")

        # Врачи
        doctors = []
        for i, spec in enumerate(SPECIALIZATIONS):
            gender = random.choice(["M", "F"])
            last = random.choice(LAST_NAMES if gender == "M" else FEMALE_LAST_NAMES)
            first = random.choice(MALE_FIRST_NAMES if gender == "M" else FEMALE_FIRST_NAMES)
            phone = random.choice(PHONES)
            doctor = Doctor.objects.create(
                last_name=last,
                first_name=first,
                specialization=spec,
                phone=phone,
                email=f"doctor{i+1}@clinic.ru",
            )
            doctors.append(doctor)
        self.stdout.write(f"  Создано врачей: {len(doctors)}")

        # Пациенты
        patients = []
        for i in range(30):
            gender = random.choice(["M", "F"])
            last = random.choice(LAST_NAMES if gender == "M" else FEMALE_LAST_NAMES)
            first = random.choice(MALE_FIRST_NAMES if gender == "M" else FEMALE_FIRST_NAMES)
            phone = random.choice(PHONES)
            patient = Patient.objects.create(
                last_name=last,
                first_name=first,
                date_of_birth=random_date(),
                phone=phone,
                email=f"patient{i+1}@mail.ru" if random.random() > 0.3 else "",
                address=f"г. Москва, ул. {random.choice(LAST_NAMES)+'а'}, д. {random.randint(1, 99)}, кв. {random.randint(1, 200)}",
            )
            patients.append(patient)
        self.stdout.write(f"  Создано пациентов: {len(patients)}")

        # Медицинские записи
        records_count = 0
        for patient in patients:
            for _ in range(random.randint(2, 6)):
                MedicalRecord.objects.create(
                    patient=patient,
                    doctor=random.choice(doctors),
                    title=random.choice(RECORD_TITLES),
                    description=random.choice(DESCRIPTIONS),
                    diagnosis=random.choice(DIAGNOSES),
                )
                records_count += 1
        self.stdout.write(f"  Создано записей: {records_count}")

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена."))
