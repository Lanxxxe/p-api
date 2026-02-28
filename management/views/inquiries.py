from django.shortcuts import render, redirect
from django.contrib import messages
from management.models import Manager, IssueReport


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


def inquiries(request):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    issue_reports = IssueReport.objects.select_related('manager').all()

    return render(request, 'inquiries.html', {
        'manager': manager,
        'issue_reports': issue_reports,
        'total_reports': issue_reports.count(),
        'open_reports': issue_reports.filter(status=IssueReport.STATUS_OPEN).count(),
        'resolved_reports': issue_reports.filter(status=IssueReport.STATUS_RESOLVED).count(),
    })
