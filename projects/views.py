from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Project
from .forms import ProjectForm


def project_list(request):
    queryset = Project.objects.all().order_by('-created_at')
    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'projects/project_list.html', {'projects': page_obj})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user_participates = (
        request.user in project.participants.all()
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
            return redirect(f'/projects/{project.pk}/')
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
            return redirect(f'/projects/{project.pk}/')
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
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if project.status != 'open':
        return JsonResponse({'status': 'error'}, status=400)
    project.status = 'closed'
    project.save()
    return JsonResponse({'status': 'ok', 'project_status': 'closed'})


@require_POST
@login_required
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project in request.user.favorites.all():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({'status': 'ok', 'favorited': favorited})


@require_POST
@login_required
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user == project.owner:
        return JsonResponse(
            {'status': 'error', 'message': 'Owner cannot leave project'},
            status=400
        )
    if request.user in project.participants.all():
        project.participants.remove(request.user)
        participating = False
    else:
        project.participants.add(request.user)
        participating = True
    return JsonResponse({'status': 'ok', 'participating': participating})


@login_required
def favorites_list(request):
    projects = request.user.favorites.all().order_by('-created_at')
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'projects/favorite_projects.html', {'projects': page_obj})
