from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from management.models import Manager, IssueReport


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
                request.session['manager_role'] = manager.role
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


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Validation
        if not username or not password:
            return render(request, 'register.html', {
                'error': 'Username and password are required.',
                'form': request.POST,
            })

        if password != confirm_password:
            return render(request, 'register.html', {
                'error': 'Passwords do not match.',
                'form': request.POST,
            })

        if len(password) < 8:
            return render(request, 'register.html', {
                'error': 'Password must be at least 8 characters long.',
                'form': request.POST,
            })

        if Manager.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'That username is already taken.',
                'form': request.POST,
            })

        if email and Manager.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'An account with that email already exists.',
                'form': request.POST,
            })

        Manager.objects.create(
            username=username,
            email=email or None,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password),
        )

        return render(request, 'login.html', {
            'success': 'Account created successfully. You can now sign in.'
        })

    return render(request, 'register.html')


def profile(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')

    manager = Manager.objects.get(id=manager_id)
    error = None
    success = None
    active_tab = request.POST.get('active_tab', 'profile')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # ── Profile info ──────────────────────────────────────────────
        if form_type == 'profile':
            manager.first_name = request.POST.get('first_name', '').strip()
            manager.last_name  = request.POST.get('last_name', '').strip()
            manager.email      = request.POST.get('email', '').strip() or None
            manager.bio        = request.POST.get('bio', '').strip() or None
            manager.avatar_url = request.POST.get('avatar_url', '').strip() or None

            # Check email uniqueness (excluding self)
            email = request.POST.get('email', '').strip()
            if email and Manager.objects.filter(email=email).exclude(id=manager_id).exists():
                error = 'That email is already in use by another account.'
                active_tab = 'profile'
            else:
                manager.save()
                success = 'Profile updated successfully.'
                active_tab = 'profile'

        # ── Internship settings ───────────────────────────────────────
        elif form_type == 'internship':
            manager.internship_role       = request.POST.get('internship_role', '').strip() or None
            manager.company               = request.POST.get('company', '').strip() or None
            manager.school                = request.POST.get('school', '').strip() or None
            manager.course                = request.POST.get('course', '').strip() or None
            manager.total_hours_needed    = int(request.POST.get('total_hours_needed') or 486)
            start_date = request.POST.get('internship_start_date', '').strip()
            manager.internship_start_date = start_date if start_date else None
            manager.save()
            success = 'Internship settings saved.'
            active_tab = 'internship'

        # ── Change password ───────────────────────────────────────────
        elif form_type == 'password':
            current_pw  = request.POST.get('current_password', '')
            new_pw      = request.POST.get('new_password', '')
            confirm_pw  = request.POST.get('confirm_password', '')
            active_tab  = 'password'

            if not check_password(current_pw, manager.password):
                error = 'Current password is incorrect.'
            elif new_pw != confirm_pw:
                error = 'New passwords do not match.'
            elif len(new_pw) < 8:
                error = 'New password must be at least 8 characters.'
            else:
                manager.password = make_password(new_pw)
                manager.save()
                success = 'Password changed successfully.'

    return render(request, 'profile.html', {
        'manager': manager,
        'active_tab': active_tab,
        'error': error,
        'success': success,
    })


def submit_issue(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    if request.method == 'POST':
        manager_id = request.session.get('manager_id')
        manager = Manager.objects.filter(id=manager_id).first()
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', IssueReport.CATEGORY_BUG)

        if title and description:
            IssueReport.objects.create(
                manager=manager,
                title=title,
                description=description,
                category=category,
            )

    return redirect('profile')