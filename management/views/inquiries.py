from django.shortcuts import render


def inquiries(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'inquiries.html')
