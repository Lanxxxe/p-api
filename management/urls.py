from django.urls import path
from .views import auth, dashboard, projects, achievements, tools, inquiries, internship

urlpatterns = [
    path('', auth.login, name='login'),
    path('dashboard/', dashboard.dashboard, name='dashboard'),


    # Project
    path('projects/', projects.projects, name='projects'),
    path('projects/add/', projects.add_project, name='add_project'),
    path('projects/edit/<int:project_id>/', projects.edit_project, name='edit_project'),
    path('projects/delete/<int:project_id>/', projects.delete_project, name='delete_project'),

    # Achievement
    path('achievements/', achievements.achievements, name='achievements'),
    path('achievements/add/', achievements.add_achievement, name='add_achievement'),
    path('achievements/edit/', achievements.edit_achievement, name='edit_achievement'),
    # path('achievements/delete/', views.delete_achievement, name='delete_achievement'),

    # Tools
    path('tools/', tools.tools, name='tools'),
    path('tools/add/', tools.add_tool, name='add_tool'),
    path('tools/edit/', tools.edit_tool, name='edit_tool'),
    # path('tools/delete/', views.delete_tool, name='delete_tool'),

    # Inquiries
    path('inquiries/', inquiries.inquiries, name='inquiries'),

    # Internship
    path('internship/', internship.internship, name='internship'),
    path('internship/create/', internship.log_create, name='internship-log-create'),
    path('internship/statistics/', internship.log_statistics, name='internship-log-statistics'),
    path('internship/<int:log_id>/', internship.log_detail, name='internship-log-detail'),
    path('internship/<int:log_id>/update/', internship.log_update, name='internship-log-update'),
    path('internship/<int:log_id>/delete/', internship.log_delete, name='internship-log-delete'),

    path('logout/', auth.logout, name='logout'),
]
