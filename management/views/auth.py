from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from management.models import Manager


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        try: 
            manager = Manager.objects.get(username=username)
            if check_password(password, manager.password):
                # Set session
                request.session['manager_id'] = manager.id
                request.session['manager_username'] = manager.username
                request.session['is_authenticated'] = True
                
                if remember:
                    # 2 Weeks
                    request.session.set_expiry(1209600)
                else:
                    # Browser Close
                    request.session.set_expiry(0)

                return redirect('dashboard')
            else:
                return render(request, 'login.html', {
                    'error': 'Invalid username or password. Access denied.'
                })
        except Manager.DoesNotExist: 
            return render(request, 'login.html', {
                'error': 'Invalid username or password. Access denied.'
            })
    
    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('login')