from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from datetime import date, datetime, timedelta
from django.core.paginator import Paginator
from management.models import InternshipLog
from management.services import InternshipService

def internship(request):    
    total_hours_needed = 486
    total_hours = InternshipService.calculate_total_hours()
    remaining_hours = InternshipService.calculate_remaining_hours(total_hours_needed)
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
        current_end = current_start + timedelta(days=4)  # Friday (Monday + 4 days)
        weeks.append({
            'start': current_start,
            'end': current_end,
            'label': f"{current_start.strftime('%B %d')} - {current_end.strftime('%d, %Y')}",
            'value': current_start.strftime('%Y-%m-%d')
        })
        current_start += timedelta(days=7)  # Next Monday
    
    # Determine which week to display
    if filter_week:
        try:
            start_of_week = datetime.strptime(filter_week, '%Y-%m-%d').date()
            end_of_week = start_of_week + timedelta(days=4)  # Friday
        except ValueError:
            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=4)
    else:
        # Default to current week
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=4)  # Friday
    
    # Filter logs for selected week
    logs = InternshipLog.objects.filter(
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
            photos = request.FILES.get('photos', None)


            log_created = InternshipLog.objects.create(
                date=log_date,
                time_in=time_in,
                time_out=time_out,
                notes=notes,
                photos=photos
            )
            
            messages.success(request, 'Log added successfully!')
            
            return redirect('internship')
        except Exception as e:
            messages.error(request, f'Error adding log: {str(e)}')
            return redirect('internship')
    
    return render(request, 'internship/create_logs.html')


def log_detail(request, log_id):
    """Get log details"""
    log = get_object_or_404(InternshipLog, id=log_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'id': log.id,
            'date': log.date.strftime('%Y-%m-%d'),
            'time_in': log.time_in.strftime('%H:%M'),
            'time_out': log.time_out.strftime('%H:%M'),
            'hours': float(log.hours),
            'notes': log.notes,
            'photos': log.photos.url if log.photos else ''
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def log_update(request, log_id):
    """Update a log"""
    log = get_object_or_404(InternshipLog, id=log_id)
    
    if request.method == 'POST':
        try:
            log.date = datetime.strptime(request.POST.get('log_date'), '%Y-%m-%d').date()
            log.time_in = datetime.strptime(request.POST.get('time_in'), '%H:%M').time()
            log.time_out = datetime.strptime(request.POST.get('time_out'), '%H:%M').time()
            log.notes = request.POST.get('notes')
            
            # Handle photo upload if provided
            if request.FILES.get('photos'):
                log.photos = request.FILES.get('photos')
            
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


def log_statistics(request):
    """Get summary statistics"""
    queryset = InternshipLog.objects.all()
    
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
    total_photos = queryset.exclude(photos='').exclude(photos=None).count()
    
    # Determine status based on recent activity
    latest_log = queryset.order_by('-date').first()
    status = 'ACTIVE' if latest_log and latest_log.date >= date(2026, 2, 5) else 'INACTIVE'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'total_days': total_days,
            'total_hours': round(float(total_hours), 2),
            'total_photos': total_photos,
            'status': status
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

