from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from datetime import date, datetime, timedelta
from django.core.paginator import Paginator
from management.models import InternshipLog, Manager
from management.services import InternshipService, WeeklyNotesService
from management.gemini import enhance_note, summarize_week_notes, GeminiError, GeminiRateLimitError

def internship(request):
    manager_id = request.session.get('manager_id')
    manager = Manager.objects.filter(id=manager_id).first() if manager_id else None
    total_hours_needed = manager.total_hours_needed if manager else 486
    total_hours = InternshipService.calculate_total_hours(manager_id=manager_id)
    remaining_hours = InternshipService.calculate_remaining_hours(total_hours_needed, manager_id=manager_id)
    remaining_days = InternshipService.calculate_remaining_days(remaining_hours)
    completion_date = InternshipService.calculate_estimated_completion_date(remaining_hours)

    completion_date_obj = datetime.strptime(str(completion_date), '%Y-%m-%d') if completion_date else None

    # Get filter parameter
    filter_week = request.GET.get('week', '')
    
    # Generate list of all weeks in the current year (Monday to Friday)
    today = date.today()
    current_year = today.year
    weeks = []
    
    # Start from the first Monday of the year
    start_of_year = date(current_year, 1, 1)
    
    # Find the first Monday
    days_until_monday = (7 - start_of_year.weekday()) % 7
    if start_of_year.weekday() != 0:  # If Jan 1 is not Monday
        current_start = start_of_year + timedelta(days=days_until_monday)
    else:
        current_start = start_of_year
    
    # Generate all weeks for the year
    end_of_year = date(current_year, 12, 31)
    
    while current_start <= end_of_year:
        current_end = current_start + timedelta(days=6)  # Sunday (Monday + 6 days)
        weeks.append({
            'start': current_start,
            'end': current_end,
            'label': f"{current_start.strftime('%B %d')} - {current_end.strftime('%B %d, %Y')}",
            'value': current_start.strftime('%Y-%m-%d')
        })
        current_start += timedelta(days=7)  # Next Monday
    
    # Determine which week to display
    if filter_week:
        try:
            start_of_week = datetime.strptime(filter_week, '%Y-%m-%d').date()
            end_of_week = start_of_week + timedelta(days=6)  # Sunday
        except ValueError:
            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
    else:
        # Default to current week
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
    
    # Filter logs for selected week — scoped to current manager
    logs = InternshipLog.objects.filter(
        manager_id=manager_id,
        date__gte=start_of_week,
        date__lte=end_of_week
    ).order_by('-date', '-time_in')
    
    # Pagination - 7 results per page
    paginator = Paginator(logs, 7)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'logs': page_obj,
        'total_hours_needed': total_hours_needed,
        'total_hours': round(total_hours, 2),
        'remaining_hours': round(remaining_hours, 2),
        'remaining_days': round(remaining_days, 2),
        'completion_date': completion_date_obj.strftime('%B %d, %Y') if completion_date_obj else 'N/A',
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'weeks': weeks,
        'selected_week': filter_week or start_of_week.strftime('%Y-%m-%d')
    }
    
    return render(request, 'internship.html', context)


def log_create(request):
    """Create a new log"""
    if request.method == 'POST':
        try:
            
            data = request.POST
            log_date = datetime.strptime(data.get('log_date'), '%Y-%m-%d').date()
            time_in = datetime.strptime(data.get('time_in'), '%H:%M').time()
            time_out = datetime.strptime(data.get('time_out'), '%H:%M').time()
            notes = data.get('notes', 'No Notes for this log.')

            manager_id = request.session.get('manager_id')
            manager = Manager.objects.filter(id=manager_id).first() if manager_id else None

            # Prevent duplicate log for the same day
            if InternshipLog.objects.filter(manager_id=manager_id, date=log_date).exists():
                messages.error(request, 'A log for this date already exists.')
                return redirect('internship')

            log_created = InternshipLog.objects.create(
                manager=manager,
                date=log_date,
                time_in=time_in,
                time_out=time_out,
                notes=notes,
            )
            
            messages.success(request, 'Log added successfully!')
            
            return redirect('internship')
        except Exception as e:
            messages.error(request, f'Error adding log: {str(e)}')
            return redirect('internship')
    
    return render(request, 'internship/create_logs.html')


def log_detail(request, log_id):
    """Show full log detail page"""
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')

    log = get_object_or_404(InternshipLog, id=log_id, manager_id=manager_id)
    return render(request, 'internship/detailed_log.html', {'log': log})


def enhance_log_note(request, log_id):
    """Enhance the note of a log using Gemini and return the enhanced text."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

    manager_id = request.session.get('manager_id')
    if not manager_id:
        return JsonResponse({'error': 'Unauthenticated.'}, status=401)

    log = get_object_or_404(InternshipLog, id=log_id, manager_id=manager_id)

    daily = WeeklyNotesService.get_daily_note(manager_id=manager_id, day=log.date)
    notes = daily['notes'] if daily else (log.notes or '')

    if not notes.strip():
        return JsonResponse({'error': 'No notes to enhance.'}, status=400)

    manager = Manager.objects.filter(id=manager_id).first()
    internship_role = (manager.internship_role or 'Intern') if manager else 'Intern'

    AI_REQUEST_LIMIT = 2
    if manager and manager.ai_requests_used >= AI_REQUEST_LIMIT:
        return JsonResponse(
            {'error': f'You have reached the {AI_REQUEST_LIMIT} AI request limit for your account.'},
            status=403,
        )

    try:
        enhanced = enhance_note(notes=notes, internship_role=internship_role)
        # Only increment AFTER a confirmed successful response
        if manager:
            manager.ai_requests_used += 1
            manager.save(update_fields=['ai_requests_used'])
        return JsonResponse({'enhanced': enhanced, 'requests_used': manager.ai_requests_used if manager else None})
    except GeminiRateLimitError as e:
        # Gemini quota hit — do NOT consume the user's in-app request count
        return JsonResponse({'error': str(e)}, status=429)
    except GeminiError as e:
        # Service down, timeout, empty response, etc. — also don't consume count
        return JsonResponse({'error': str(e)}, status=502)
    except Exception:
        return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)


def save_log_note(request, log_id):
    """Save an updated note text to a log (AJAX)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

    manager_id = request.session.get('manager_id')
    if not manager_id:
        return JsonResponse({'error': 'Unauthenticated.'}, status=401)

    log = get_object_or_404(InternshipLog, id=log_id, manager_id=manager_id)

    import json
    try:
        body = json.loads(request.body)
        new_notes = body.get('notes', '').strip()
    except (ValueError, KeyError):
        return JsonResponse({'error': 'Invalid request body.'}, status=400)

    if not new_notes:
        return JsonResponse({'error': 'Notes cannot be empty.'}, status=400)

    log.notes = new_notes
    log.save(update_fields=['notes'])
    return JsonResponse({'success': True})


def summarize_week(request):
    """Summarize all notes for the given week using Gemini (AJAX)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

    manager_id = request.session.get('manager_id')
    if not manager_id:
        return JsonResponse({'error': 'Unauthenticated.'}, status=401)

    import json
    try:
        body = json.loads(request.body)
        week_start_str = body.get('week_start', '').strip()
    except (ValueError, KeyError):
        return JsonResponse({'error': 'Invalid request body.'}, status=400)

    try:
        start_of_week = datetime.strptime(week_start_str, '%Y-%m-%d').date()
    except ValueError:
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())

    end_of_week = start_of_week + timedelta(days=6)

    logs = InternshipLog.objects.filter(
        manager_id=manager_id,
        date__gte=start_of_week,
        date__lte=end_of_week,
    ).exclude(notes__isnull=True).exclude(notes='').order_by('date')

    if not logs.exists():
        return JsonResponse({'error': 'No notes found for this week to summarize.'}, status=400)

    manager = Manager.objects.filter(id=manager_id).first()
    internship_role = (manager.internship_role or 'Intern') if manager else 'Intern'

    AI_REQUEST_LIMIT = 2
    if manager and manager.ai_requests_used >= AI_REQUEST_LIMIT:
        return JsonResponse(
            {'error': f'You have reached the {AI_REQUEST_LIMIT} AI request limit for your account.'},
            status=403,
        )

    week_label = f"{start_of_week.strftime('%B %d')} – {end_of_week.strftime('%B %d, %Y')}"

    notes_entries = [
        {
            'day_name': log.date.strftime('%A'),
            'date': log.date.strftime('%B %d, %Y'),
            'notes': log.notes,
        }
        for log in logs
    ]

    try:
        summary = summarize_week_notes(
            notes_entries=notes_entries,
            week_label=week_label,
            internship_role=internship_role,
        )
        # Only increment AFTER a confirmed successful response
        if manager:
            manager.ai_requests_used += 1
            manager.save(update_fields=['ai_requests_used'])
        return JsonResponse({'summary': summary, 'requests_used': manager.ai_requests_used if manager else None})
    except GeminiRateLimitError as e:
        # Gemini quota hit — do NOT consume the user's in-app request count
        return JsonResponse({'error': str(e)}, status=429)
    except GeminiError as e:
        # Service down, timeout, empty response, etc. — also don't consume count
        return JsonResponse({'error': str(e)}, status=502)
    except Exception:
        return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)


def log_update(request, log_id):
    """Update a log"""
    log = get_object_or_404(InternshipLog, id=log_id)
    
    if request.method == 'POST':
        try:
            log.date = datetime.strptime(request.POST.get('log_date'), '%Y-%m-%d').date()
            log.time_in = datetime.strptime(request.POST.get('time_in'), '%H:%M').time()
            log.time_out = datetime.strptime(request.POST.get('time_out'), '%H:%M').time()
            log.notes = request.POST.get('notes')
            log.save()
            messages.success(request, 'Log updated successfully!')
            return redirect('internship')
        except Exception as e:
            messages.error(request, f'Error updating log: {str(e)}')
            return redirect('internship')
    

    return render(request, 'internship/update_logs.html', {'log': log})


def log_delete(request, log_id):
    """Delete a log"""
    log = get_object_or_404(InternshipLog, id=log_id)
    
    if request.method == 'POST':
        try:
            log.delete()
            messages.success(request, 'Log deleted successfully!')
            return redirect('internship')
        except Exception as e:
            messages.error(request, f'Error deleting log: {str(e)}')
            return redirect('internship')
    
    return redirect('internship')


def quick_timein(request):
    """Store time-in for today in the session."""
    if request.method != 'POST':
        return redirect('dashboard')

    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')

    today = date.today()

    if InternshipLog.objects.filter(manager_id=manager_id, date=today).exists():
        messages.error(request, 'You already have a log for today.')
        return redirect('dashboard')

    now = datetime.now()
    request.session['timein_date'] = str(today)
    request.session['timein_time'] = now.strftime('%H:%M')
    messages.success(request, f'Time-in recorded at {now.strftime("%I:%M %p")}.')
    return redirect('dashboard')


def quick_timeout(request):
    """Create today\'s log using the session-stored time-in and current time."""
    if request.method != 'POST':
        return redirect('dashboard')

    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')

    timein_date = request.session.get('timein_date')
    timein_time = request.session.get('timein_time')
    today = date.today()

    if not timein_date or not timein_time:
        messages.error(request, 'No active time-in found. Please time in first.')
        return redirect('dashboard')

    if timein_date != str(today):
        request.session.pop('timein_date', None)
        request.session.pop('timein_time', None)
        messages.error(request, 'Time-in session expired. Please time in again.')
        return redirect('dashboard')

    if InternshipLog.objects.filter(manager_id=manager_id, date=today).exists():
        request.session.pop('timein_date', None)
        request.session.pop('timein_time', None)
        messages.error(request, 'A log for today already exists.')
        return redirect('dashboard')

    manager = Manager.objects.filter(id=manager_id).first()
    now = datetime.now()
    time_in = datetime.strptime(timein_time, '%H:%M').time()
    time_out = now.time().replace(second=0, microsecond=0)

    notes = request.POST.get('notes', '').strip() or 'Quick log from dashboard.'
    InternshipLog.objects.create(
        manager=manager,
        date=today,
        time_in=time_in,
        time_out=time_out,
        notes=notes,
    )

    request.session.pop('timein_date', None)
    request.session.pop('timein_time', None)
    messages.success(request, f'Time-out recorded at {now.strftime("%I:%M %p")}. Log saved!')
    return redirect('dashboard')


def log_statistics(request):
    """Get summary statistics — scoped to current manager"""
    manager_id = request.session.get('manager_id')
    queryset = InternshipLog.objects.filter(manager_id=manager_id) if manager_id else InternshipLog.objects.none()
    
    # Apply date filters if provided
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    
    # Calculate statistics
    total_days = queryset.count()
    total_hours = queryset.aggregate(total=Sum('hours'))['total'] or 0
    
    # Determine status based on recent activity
    latest_log = queryset.order_by('-date').first()
    status = 'ACTIVE' if latest_log and latest_log.date >= date(2026, 2, 5) else 'INACTIVE'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'total_days': total_days,
            'total_hours': round(float(total_hours), 2),
            'status': status
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

