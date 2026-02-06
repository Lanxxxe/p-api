from django.shortcuts import render


def dashboard(request):
    # Check if manager is authenticated
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'dashboard.html')
    