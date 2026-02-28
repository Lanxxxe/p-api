from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from management.models import Achievement, Manager


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


def achievements(request):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    achievements = Achievement.objects.filter(manager=manager).order_by('-date_achieved')
    categories = set()
    for a in achievements:
        if a.category:
            categories.update(a.category)

    return render(request, 'achievements.html', {
        'achievements': achievements,
        'total': achievements.count(),
        'total_categories': len(categories),
    })


def add_achievement(request):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    if request.method == 'POST':
        try:
            Achievement.objects.create(
                manager=manager,
                event=request.POST.get('event'),
                ranked=request.POST.get('ranked'),
                summary=request.POST.get('summary'),
                description=request.POST.get('description'),
                location=request.POST.get('location'),
                date_achieved=request.POST.get('date_achieved'),
                proof_url=request.POST.get('proof_url'),
                category=request.POST.getlist('category'),
            )
            messages.success(request, 'Achievement added successfully.')
            return redirect('achievements')
        except Exception as e:
            return render(request, 'achievements_features/add_achievement.html', {'error': str(e)})

    return render(request, 'achievements_features/add_achievement.html')


def edit_achievement(request, achievement_id):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    achievement = get_object_or_404(Achievement, id=achievement_id, manager=manager)

    if request.method == 'POST':
        achievement.event = request.POST.get('event')
        achievement.ranked = request.POST.get('ranked')
        achievement.summary = request.POST.get('summary')
        achievement.description = request.POST.get('description')
        achievement.location = request.POST.get('location')
        achievement.date_achieved = request.POST.get('date_achieved')
        achievement.proof_url = request.POST.get('proof_url')
        achievement.category = request.POST.getlist('category')
        achievement.save()
        messages.success(request, 'Achievement updated successfully.')
        return redirect('achievements')

    return render(request, 'achievements_features/edit_achievement.html', {'achievement': achievement})


def delete_achievement(request, achievement_id):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    achievement = get_object_or_404(Achievement, id=achievement_id, manager=manager)
    achievement.delete()
    messages.success(request, 'Achievement deleted successfully.')
    return redirect('achievements')
