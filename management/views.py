from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from management.models import Manager
from django.contrib.auth.hashers import check_password

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        try: 
            manager = Manager.objects.get(username=username)
            if check_password(password, manager.password):
                # Set session
                request.session['manager_id'] = manager.id
                request.session['manager_username'] = manager.username
                request.session['is_authenticated'] = True
                
                if remember:
                    # 2 Weeks
                    request.session.set_expiry(1209600)
                else:
                    # Browser Close
                    request.session.set_expiry(0)

                return redirect('dashboard')
            else:
                return render(request, 'login.html', {
                    'error': 'Invalid username or password. Access denied.'
                })
        except Manager.DoesNotExist: 
            return render(request, 'login.html', {
                'error': 'Invalid username or password. Access denied.'
            })
    
    return render(request, 'login.html')

def dashboard(request):
    # Check if manager is authenticated
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'dashboard.html')

def projects(request):
    # Check if manager is authenticated
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'projects.html')

def add_project(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'projects_features/add_project.html')

def edit_project(request, project_id):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')

    print(f"Editing project with ID: {project_id}")    
    return render(request, 'projects_features/edit_project.html', {'project_id': project_id})

def achievements(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'achievements.html')

def add_achievement(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'achievements_features/add_achievement.html')

def edit_achievement(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'achievements_features/edit_achievement.html')

def tools(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'tools.html')

def add_tool(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'tools_features/add_tool.html')

def edit_tool(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'tools_features/edit_tool.html')

def inquiries(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'inquiries.html')

def internship(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'internship.html')

def logout(request):
    # Clear session
    request.session.flush()
    return redirect('login')