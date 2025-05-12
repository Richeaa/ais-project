from django.shortcuts import render, redirect
from .models import Profile

# Create your views here.
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('signin')
    return render(request, 'dashboard.html', {'username': request.session.get('username')})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = Profile.objects.get(username=username)
            if user.password == password:
                request.session['user_id'] = user.profile_id  # optional: store session
                request.session['username'] = user.username
                return redirect('dashboard')
            else:
                return render(request, 'signin.html', {'error': 'Incorrect password'})
        except Profile.DoesNotExist:
            return render(request, 'signin.html', {'error': 'User does not exist'})

    return render(request, 'signin.html')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['username']
    return redirect('signin')

