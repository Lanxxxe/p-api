from django.shortcuts import render

def achievements(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'achievements.html')

def add_achievement(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'achievements_features/add_achievement.html')

def edit_achievement(request):
    # if not request.session.get('is_authenticated'):
    #     return redirect('login')
    
    return render(request, 'achievements_features/edit_achievement.html')
