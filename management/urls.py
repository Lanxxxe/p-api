from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Project
    path('projects/', views.projects, name='projects'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/edit/<int:project_id>/', views.edit_project, name='edit_project'),

    # Achievement
    path('achievements/', views.achievements, name='achievements'),
    path('achievements/add/', views.add_achievement, name='add_achievement'),
    path('achievements/edit/', views.edit_achievement, name='edit_achievement'),
    # path('achievements/delete/', views.delete_achievement, name='delete_achievement'),

    # Tools
    path('tools/', views.tools, name='tools'),
    path('tools/add/', views.add_tool, name='add_tool'),
    path('tools/edit/', views.edit_tool, name='edit_tool'),
    # path('tools/delete/', views.delete_tool, name='delete_tool'),

    # Inquiries
    path('inquiries/', views.inquiries, name='inquiries'),

    # Internship
    path('internship/', views.internship, name='internship'),

    path('logout/', views.logout, name='logout'),
]
