from django.shortcuts import render, redirect
from .models import Profile
from .form import productForm, ReportForm

# Create your views here.
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('signin')
    return render(request, 'dashboard.html', {'username': request.session.get('username')})

def form_view(request):
    success = False
    if request.method == 'POST':
        form = productForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = productForm() 
    else:
        form = productForm()
    return render(request, 'form.html', {'form': form, 'success': success})


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

def stock(request):
    return render(request, 'stock.html')

def report_view(request):
    success = False
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user_id = request.session['user_id']  # Link to logged-in user
            report.save()
            success = True
            form = ReportForm()  # Reset the form after submit
    else:
        form = ReportForm()
    return render(request, 'report.html', {'form': form, 'success': success})