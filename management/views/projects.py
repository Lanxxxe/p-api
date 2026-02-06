from django.shortcuts import render, redirect
from django.contrib import messages
from management.models import Project
from management.serializer import ProjectSerializer
from management.services import ProjectService

def projects(request):
    projects = Project.objects.all()
    

    context = {
        'projects': projects
    }

    return render(request, 'projects.html', context)

def add_project(request):
    
    if request.method == 'POST':
        try:
            # Collect form data
            data = {
                'project_name': request.POST.get('project_name'),
                'summary': request.POST.get('summary'),
                'description': request.POST.get('description'),
                'languages': request.POST.get('languages'),
                'project_url': request.POST.get('project_url'),
                'project_image': request.POST.get('project_image'),
                'category': request.POST.getlist('category')  # Get all checked checkboxes
            }
            
            # Create project using service
            project = ProjectService.create_project(data)
            
            messages.success(request, f'Project "{project.project_name}" created successfully!')
            return redirect('projects')
            
        except ValueError as e:
            messages.error(request, f'Validation error: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error creating project: {str(e)}')
    
    return render(request, 'projects_features/add_project.html')

def edit_project(request, project_id):
   
    return render(request, 'projects_features/edit_project.html', {'project_id': project_id})


def delete_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        project.delete()
        messages.success(request, f'Project "{project.project_name}" deleted successfully!')
    except Project.DoesNotExist:
        messages.error(request, 'Project not found.')
    except Exception as e:
        messages.error(request, f'Error deleting project: {str(e)}')
    
    return redirect('projects')

