from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User
from .forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/projects/list/')
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
                return redirect('/projects/list/')
            else:
                form.add_error(None, 'Неверный имейл или пароль')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/projects/list/')


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user-details.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(f'/users/{request.user.pk}/')
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
            return redirect(f'/users/{request.user.pk}/')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})


def users_list(request):
    queryset = User.objects.all().order_by('id')
    active_filter = None

    if request.user.is_authenticated:
        active_filter = request.GET.get('filter', None)

        if active_filter == 'favorite_authors':
            favorite_projects = request.user.favorites.all()
            queryset = User.objects.filter(
                owned_projects__in=favorite_projects
            ).distinct().order_by('id')

        elif active_filter == 'participated_projects_authors':
            participated_projects = request.user.participated_projects.all()
            queryset = User.objects.filter(
                owned_projects__in=participated_projects
            ).distinct().order_by('id')

        elif active_filter == 'interested_in_my_projects':
            my_projects = request.user.owned_projects.all()
            queryset = User.objects.filter(
                favorites__in=my_projects
            ).distinct().order_by('id')

        elif active_filter == 'my_project_participants':
            my_projects = request.user.owned_projects.all()
            queryset = User.objects.filter(
                participated_projects__in=my_projects
            ).distinct().order_by('id')

        else:
            active_filter = None

    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/participants.html', {
        'participants': page_obj,
        'active_filter': active_filter,
    })
