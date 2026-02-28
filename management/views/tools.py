from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from management.models import Tool, Manager


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


def tools(request):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    tools = Tool.objects.filter(manager=manager).order_by('tool_name')
    categories = set()
    for t in tools:
        if t.category:
            categories.update(t.category)

    return render(request, 'tools.html', {
        'tools': tools,
        'total': tools.count(),
        'total_categories': len(categories),
    })


def add_tool(request):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    if request.method == 'POST':
        try:
            Tool.objects.create(
                manager=manager,
                tool_name=request.POST.get('tool_name'),
                description=request.POST.get('description'),
                version=request.POST.get('version'),
                icon_url=request.POST.get('icon_url', ''),
                category=request.POST.getlist('category'),
            )
            messages.success(request, 'Tool added successfully.')
            return redirect('tools')
        except Exception as e:
            return render(request, 'tools_features/add_tool.html', {'error': str(e)})

    return render(request, 'tools_features/add_tool.html')


def edit_tool(request, tool_id):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    tool = get_object_or_404(Tool, id=tool_id, manager=manager)

    if request.method == 'POST':
        tool.tool_name = request.POST.get('tool_name')
        tool.description = request.POST.get('description')
        tool.version = request.POST.get('version')
        tool.icon_url = request.POST.get('icon_url', '')
        tool.category = request.POST.getlist('category')
        tool.save()
        messages.success(request, 'Tool updated successfully.')
        return redirect('tools')

    return render(request, 'tools_features/edit_tool.html', {'tool': tool})


def delete_tool(request, tool_id):
    denied, manager = _supervisor_only(request)
    if denied:
        return denied

    tool = get_object_or_404(Tool, id=tool_id, manager=manager)
    tool.delete()
    messages.success(request, 'Tool deleted successfully.')
    return redirect('tools')
