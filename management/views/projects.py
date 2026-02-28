from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from management.models import Project, Manager
from management.serializer import ProjectSerializer
from management.services import ProjectService


def _supervisor_only(request):
    """Returns (None, manager) for supervisors, or (redirect, None) if denied."""
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login'), None
    manager = Manager.objects.filter(id=manager_id).first()
    if not manager:
        return redirect('login'), None
    if manager.role != Manager.SUPERVISOR:
        messages.error(request, 'Access restricted to supervisors only.')
        return redirect('dashboard'), None
    return None, manager


def projects(request):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    projects = Project.objects.filter(manager=manager).order_by('-created_at')
    return render(request, 'projects.html', {'projects': projects})


def add_project(request):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    if request.method == 'POST':
        try:
            data = {
                'project_name': request.POST.get('project_name'),
                'summary': request.POST.get('summary'),
                'description': request.POST.get('description'),
                'languages': request.POST.get('languages'),
                'project_url': request.POST.get('project_url'),
                'project_image': request.POST.get('project_image'),
                'category': request.POST.getlist('category'),
            }
            project = ProjectService.create_project(data, manager=manager)
            messages.success(request, f'Project "{project.project_name}" created successfully!')
            return redirect('projects')
        except ValueError as e:
            messages.error(request, f'Validation error: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error creating project: {str(e)}')

    return render(request, 'projects_features/add_project.html')


def edit_project(request, project_id):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    project = get_object_or_404(Project, id=project_id, manager=manager)

    if request.method == 'POST':
        try:
            project.project_name  = request.POST.get('project_name', '').strip()
            project.summary       = request.POST.get('summary', '').strip()
            project.description   = request.POST.get('description', '').strip()
            project.languages     = request.POST.get('languages', '').strip()
            project.project_url  = request.POST.get('project_url', '').strip()
            project.project_image = request.POST.get('project_image', '').strip()
            project.category      = request.POST.getlist('category')
            project.save()
            messages.success(request, f'Project "{project.project_name}" updated successfully!')
            return redirect('projects')
        except Exception as e:
            messages.error(request, f'Error updating project: {str(e)}')

    return render(request, 'projects_features/edit_project.html', {
        'project': project,
    })


def delete_project(request, project_id):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    try:
        project = Project.objects.get(id=project_id, manager=manager)
        name = project.project_name
        project.delete()
        messages.success(request, f'Project "{name}" deleted successfully!')
    except Project.DoesNotExist:
        messages.error(request, 'Project not found or you do not have permission to delete it.')
    except Exception as e:
        messages.error(request, f'Error deleting project: {str(e)}')

    return redirect('projects')

