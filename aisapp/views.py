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

from .models import ProductionSchedule, ProductionIssue, Product
from django.utils import timezone

def production_plan(request):
    success = False
    if request.method == 'POST':
        product_id = request.POST.get('product')
        start_date = request.POST.get('start_date')
        estimated_end = request.POST.get('estimated_end')
        priority = request.POST.get('priority')

        ProductionSchedule.objects.create(
            product_id=int(product_id),
            start_date=start_date,
            estimated_end_date=estimated_end,
            priority=priority
        )
        success = True 

    plans = ProductionSchedule.objects.all()
    products = Product.objects.all()
    return render(request, 'production_plan.html', {'plans': plans, 'products': products, 'success': success})

def production_issue(request):
    success = False
    if request.method == 'POST':
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')

        ProductionIssue.objects.create(
            issue_type=issue_type,
            description=description
        )
        success = True 

    issues = ProductionIssue.objects.all()
    return render(request, 'production_issue.html', {'issues': issues, 'success': success})

# Edit Production Plan
def edit_production_plan(request, id):
    plan = ProductionSchedule.objects.get(id=id)
    products = Product.objects.all()
    success = False

    if request.method == 'POST':
        plan.product_id = request.POST.get('product')
        plan.start_date = request.POST.get('start_date')
        plan.estimated_end_date = request.POST.get('estimated_end')
        plan.priority = request.POST.get('priority')
        plan.save()
        success = True

    return render(request, 'edit_production_plan.html', {
        'plan': plan,
        'products': products,
        'success': success
    })

# Delete Production Plan
def delete_production_plan(request, id):
    ProductionSchedule.objects.get(id=id).delete()
    return redirect('production_plan')

# Edit Production Issue
def edit_production_issue(request, id):
    issue = ProductionIssue.objects.get(id=id)
    success = False

    if request.method == 'POST':
        issue.issue_type = request.POST.get('issue_type')
        issue.description = request.POST.get('description')
        issue.save()
        success = True

    return render(request, 'edit_production_issue.html', {
        'issue': issue,
        'success': success
    })

# Delete Production Issue
def delete_production_issue(request, id):
    ProductionIssue.objects.get(id=id).delete()
    return redirect('production_issue')
