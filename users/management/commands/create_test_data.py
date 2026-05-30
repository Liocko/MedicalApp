from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Creates test users and projects'

    @transaction.atomic
    def handle(self, *args, **options):
        from users.models import User
        from projects.models import Project

        users_data = [
            {'email': 'alice@example.com', 'name': 'Алиса', 'surname': 'Иванова',
             'about': 'Frontend-разработчик. Люблю Vue.js и красивые интерфейсы.',
             'phone': '+79001234567', 'github_url': 'https://github.com/alice'},
            {'email': 'bob@example.com', 'name': 'Борис', 'surname': 'Петров',
             'about': 'Backend Python разработчик. Django, FastAPI, PostgreSQL.',
             'phone': '+79009876543', 'github_url': 'https://github.com/bob'},
            {'email': 'carol@example.com', 'name': 'Карина', 'surname': 'Смирнова',
             'about': 'Full-stack разработчик и UI/UX дизайнер.',
             'phone': '+79001112233'},
        ]

        created_users = []
        for data in users_data:
            phone = data.pop('phone', '')
            github = data.pop('github_url', '')
            if User.objects.filter(email=data['email']).exists():
                u = User.objects.get(email=data['email'])
            else:
                u = User(**data, phone=phone, github_url=github)
                u.set_password('testpass123')
                u.save()
                self.stdout.write(f'  Created user: {u.email}')
            created_users.append(u)

        projects_data = [
            {'name': 'Маркетплейс для фрилансеров', 'owner': created_users[0],
             'description': 'Платформа для поиска заказов и фрилансеров в IT-сфере.',
             'github_url': 'https://github.com/alice/freelance-market', 'status': 'open'},
            {'name': 'Трекер задач для команд', 'owner': created_users[1],
             'description': 'Простой и удобный инструмент управления задачами.',
             'github_url': 'https://github.com/bob/task-tracker', 'status': 'open'},
            {'name': 'Агрегатор новостей', 'owner': created_users[2],
             'description': 'Собираем новости из разных источников в одном месте.',
             'status': 'open'},
            {'name': 'Мобильное приложение для спорта', 'owner': created_users[0],
             'description': 'Трекинг тренировок, питания и прогресса.',
             'status': 'closed'},
        ]

        for data in projects_data:
            owner = data['owner']
            if not Project.objects.filter(name=data['name'], owner=owner).exists():
                p = Project.objects.create(**data)
                p.participants.add(owner)
                self.stdout.write(f'  Created project: {p.name}')

        if created_users:
            u0, u1, u2 = created_users
            p0 = Project.objects.filter(owner=u0).first()
            p1 = Project.objects.filter(owner=u1).first()
            if p0:
                p0.participants.add(u1)
            if p1:
                p1.participants.add(u2)

        self.stdout.write(self.style.SUCCESS('Test data created successfully.'))
        self.stdout.write('Credentials: alice@example.com / bob@example.com / carol@example.com — password: testpass123')
