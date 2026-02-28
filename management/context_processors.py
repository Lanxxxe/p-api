from management.models import Manager

AI_REQUEST_LIMIT = 2


def ai_requests(request):
    """Inject AI request usage info into every template context."""
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return {
            'ai_requests_used': 0,
            'ai_requests_remaining': AI_REQUEST_LIMIT,
            'ai_request_limit': AI_REQUEST_LIMIT,
        }

    used = Manager.objects.filter(id=manager_id).values_list('ai_requests_used', flat=True).first() or 0
    remaining = max(AI_REQUEST_LIMIT - used, 0)

    return {
        'ai_requests_used': used,
        'ai_requests_remaining': remaining,
        'ai_request_limit': AI_REQUEST_LIMIT,
    }
