from django.shortcuts import render


def tools(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'tools.html')

def add_tool(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'tools_features/add_tool.html')

def edit_tool(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'tools_features/edit_tool.html')
