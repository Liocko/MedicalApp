from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChangePasswordForm, EditProfileForm, LoginForm, RegistrationForm
from .models import User

ITEMS_PER_PAGE = 12

FILTER_FAVORITE_AUTHORS = 'favorite_authors'
FILTER_PARTICIPATED_AUTHORS = 'participated_projects_authors'
FILTER_INTERESTED_IN_MY = 'interested_in_my_projects'
FILTER_MY_PARTICIPANTS = 'my_project_participants'


def paginate(queryset, request):
    paginator = Paginator(queryset, ITEMS_PER_PAGE)
    return paginator.get_page(request.GET.get('page'))


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('projects:list')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate_user(request)
            if user is not None:
                login(request, user)
                return redirect('projects:list')
            form.add_error(None, 'Неверный имейл или пароль')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('projects:list')


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user-details.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:detail', pk=request.user.pk)
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect('users:detail', pk=request.user.pk)
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})


def users_list(request):
    queryset = User.objects.all().order_by('id')
    active_filter = None

    if request.user.is_authenticated:
        active_filter = request.GET.get('filter')

        if active_filter == FILTER_FAVORITE_AUTHORS:
            queryset = User.objects.filter(
                owned_projects__in=request.user.favorites.all()
            ).distinct().order_by('id')

        elif active_filter == FILTER_PARTICIPATED_AUTHORS:
            queryset = User.objects.filter(
                owned_projects__in=request.user.participated_projects.all()
            ).distinct().order_by('id')

        elif active_filter == FILTER_INTERESTED_IN_MY:
            queryset = User.objects.filter(
                favorites__in=request.user.owned_projects.all()
            ).distinct().order_by('id')

        elif active_filter == FILTER_MY_PARTICIPANTS:
            queryset = User.objects.filter(
                participated_projects__in=request.user.owned_projects.all()
            ).distinct().order_by('id')

        else:
            active_filter = None

    return render(request, 'users/participants.html', {
        'participants': paginate(queryset, request),
        'active_filter': active_filter,
    })
