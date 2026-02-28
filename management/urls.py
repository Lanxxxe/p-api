from django.urls import path
from .views import auth, dashboard, projects, achievements, tools, inquiries, internship

urlpatterns = [
    path('', auth.login, name='login'),
    path('register/', auth.register, name='register'),
    path('profile/', auth.profile, name='profile'),
    path('dashboard/', dashboard.dashboard, name='dashboard'),


    # Project
    path('projects/', projects.projects, name='projects'),
    path('projects/add/', projects.add_project, name='add_project'),
    path('projects/edit/<int:project_id>/', projects.edit_project, name='edit_project'),
    path('projects/delete/<int:project_id>/', projects.delete_project, name='delete_project'),

    # Achievement
    path('achievements/', achievements.achievements, name='achievements'),
    path('achievements/add/', achievements.add_achievement, name='add_achievement'),
    path('achievements/edit/<int:achievement_id>/', achievements.edit_achievement, name='edit_achievement'),
    path('achievements/delete/<int:achievement_id>/', achievements.delete_achievement, name='delete_achievement'),

    # Tools
    path('tools/', tools.tools, name='tools'),
    path('tools/add/', tools.add_tool, name='add_tool'),
    path('tools/edit/<int:tool_id>/', tools.edit_tool, name='edit_tool'),
    path('tools/delete/<int:tool_id>/', tools.delete_tool, name='delete_tool'),

    # Inquiries
    path('inquiries/', inquiries.inquiries, name='inquiries'),

    # Internship
    path('internship/', internship.internship, name='internship'),
    path('internship/create/', internship.log_create, name='internship-log-create'),
    path('internship/statistics/', internship.log_statistics, name='internship-log-statistics'),
    path('internship/quick-timein/', internship.quick_timein, name='quick_timein'),
    path('internship/quick-timeout/', internship.quick_timeout, name='quick_timeout'),
    path('internship/summarize-week/', internship.summarize_week, name='internship-summarize-week'),
    path('internship/<int:log_id>/', internship.log_detail, name='internship-log-detail'),
    path('internship/<int:log_id>/update/', internship.log_update, name='internship-log-update'),
    path('internship/<int:log_id>/delete/', internship.log_delete, name='internship-log-delete'),
    path('internship/<int:log_id>/enhance/', internship.enhance_log_note, name='internship-log-enhance'),
    path('internship/<int:log_id>/save-note/', internship.save_log_note, name='internship-log-save-note'),

    path('logout/', auth.logout, name='logout'),

    # Issue Reports
    path('profile/report/', auth.submit_issue, name='submit_issue'),
]
