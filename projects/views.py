from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProjectForm
from .models import PROJECT_STATUS_OPEN, PROJECT_STATUS_CLOSED, Project

ITEMS_PER_PAGE = 12


def paginate(queryset, request):
    paginator = Paginator(queryset, ITEMS_PER_PAGE)
    return paginator.get_page(request.GET.get('page'))


def project_list(request):
    queryset = Project.objects.select_related('owner').all()
    return render(request, 'projects/project_list.html', {'projects': paginate(queryset, request)})


def project_detail(request, pk):
    project = get_object_or_404(Project.objects.select_related('owner'), pk=pk)
    user_participates = (
        project.participants.filter(pk=request.user.pk).exists()
        if request.user.is_authenticated
        else False
    )
    return render(request, 'projects/project-details.html', {
        'project': project,
        'user_participates': user_participates,
    })


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect('projects:detail', pk=project.pk)
        return render(request, 'projects/create-project.html', {
            'form': form,
            'is_edit': False,
        })
    form = ProjectForm()
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': False,
    })


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:detail', pk=project.pk)
        return render(request, 'projects/create-project.html', {
            'form': form,
            'is_edit': True,
        })
    form = ProjectForm(instance=project)
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': True,
    })


@require_POST
@login_required
def complete_project(request, pk):
    project = Project.objects.filter(pk=pk, owner=request.user).first()
    if project is None:
        return JsonResponse({'status': 'error'}, status=HTTPStatus.NOT_FOUND)
    if project.status != PROJECT_STATUS_OPEN:
        return JsonResponse({'status': 'error'}, status=HTTPStatus.BAD_REQUEST)
    project.status = PROJECT_STATUS_CLOSED
    project.save()
    return JsonResponse({'status': 'ok', 'project_status': PROJECT_STATUS_CLOSED})


@require_POST
@login_required
def toggle_favorite(request, pk):
    project = Project.objects.filter(pk=pk).first()
    if project is None:
        return JsonResponse({'status': 'error'}, status=HTTPStatus.NOT_FOUND)
    if request.user.favorites.filter(pk=pk).exists():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({'status': 'ok', 'favorited': favorited})


@require_POST
@login_required
def toggle_participate(request, pk):
    project = Project.objects.filter(pk=pk).first()
    if project is None:
        return JsonResponse({'status': 'error'}, status=HTTPStatus.NOT_FOUND)
    if request.user == project.owner:
        return JsonResponse(
            {'status': 'error', 'message': 'Owner cannot leave project'},
            status=HTTPStatus.BAD_REQUEST,
        )
    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        participating = False
    else:
        project.participants.add(request.user)
        participating = True
    return JsonResponse({'status': 'ok', 'participating': participating})


@login_required
def favorites_list(request):
    projects = request.user.favorites.select_related('owner').all()
    return render(request, 'projects/favorite_projects.html', {'projects': paginate(projects, request)})
