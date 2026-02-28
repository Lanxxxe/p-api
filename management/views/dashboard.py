from django.shortcuts import render, redirect
from datetime import date
from management.models import InternshipLog, Manager
from management.services import InternshipService


def dashboard(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')

    manager = Manager.objects.filter(id=manager_id).first()
    total_hours_needed = manager.total_hours_needed if manager else 486

    total_hours = InternshipService.calculate_total_hours(manager_id=manager_id)
    remaining_hours = InternshipService.calculate_remaining_hours(total_hours_needed, manager_id=manager_id)
    remaining_days = InternshipService.calculate_remaining_days(remaining_hours)
    completion_date = InternshipService.calculate_estimated_completion_date(remaining_hours)

    today = date.today()
    total_logs = InternshipLog.objects.filter(manager_id=manager_id).count()
    today_log = InternshipLog.objects.filter(manager_id=manager_id, date=today).first()
    recent_logs = InternshipLog.objects.filter(manager_id=manager_id).order_by('-date', '-time_in')[:5]

    progress_pct = min(round((total_hours / total_hours_needed) * 100, 1), 100) if total_hours_needed else 0

    # Quick time-in state from session
    timein_active = request.session.get('timein_date') == str(today)
    timein_time = request.session.get('timein_time') if timein_active else None

    return render(request, 'dashboard.html', {
        'manager': manager,
        'total_hours': round(total_hours, 2),
        'total_hours_needed': total_hours_needed,
        'remaining_hours': round(remaining_hours, 2),
        'remaining_days': round(remaining_days, 1),
        'completion_date': completion_date.strftime('%B %d, %Y') if completion_date else 'N/A',
        'total_logs': total_logs,
        'today_log': today_log,
        'recent_logs': recent_logs,
        'progress_pct': progress_pct,
        'timein_active': timein_active,
        'timein_time': timein_time,
        'today': today,
    })
