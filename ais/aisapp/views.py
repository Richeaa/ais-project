from django.shortcuts import render, redirect
from .models import Profile
from .form import productForm, ReportForm
from .models import ProductionSchedule, ProductionIssue, Product
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import io
import json
from django.views.decorators.csrf import csrf_exempt

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

def form_view(request):
    if 'user_id' not in request.session:
        return redirect('signin')
    
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

def stock(request):
    if 'user_id' not in request.session:
        return redirect('signin')
    
    return render(request, 'stock.html')

def report_view(request):
    if 'user_id' not in request.session:
        return redirect('signin')
    
    success = False
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user_id = request.session['user_id']  # Link to logged-in user
            report.save()
            success = True
            form = ReportForm()  # Reset the form after submit
    else:
        form = ReportForm()
    return render(request, 'report.html', {'form': form, 'success': success})

def production_plan(request):
    if 'user_id' not in request.session:
        return redirect('signin')
    
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
    if 'user_id' not in request.session:
        return redirect('signin')
    
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
    if 'user_id' not in request.session:
        return redirect('signin')
    
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
    if 'user_id' not in request.session:
        return redirect('signin')
    
    ProductionSchedule.objects.get(id=id).delete()
    return redirect('production_plan')

# Edit Production Issue
def edit_production_issue(request, id):
    if 'user_id' not in request.session:
        return redirect('signin')
    
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
    if 'user_id' not in request.session:
        return redirect('signin')
    
    ProductionIssue.objects.get(id=id).delete()
    return redirect('production_issue')

@csrf_exempt
def generate_document(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = data.get('product')
            user = data.get('user')
            date = data.get('date')
            status = data.get('status')

            if not all([product, user, date]):
                return HttpResponse("Missing data", content_type="text/plain", status=400)

            buffer = io.BytesIO()
            p = canvas.Canvas(buffer)
            p.drawString(100, 800, f"Produk: {product}")
            p.drawString(100, 780, f"User: {user}")
            p.drawString(100, 760, f"Tanggal: {date}")
            p.drawString(100, 740, f"Status: {status}")
            p.showPage()
            p.save()

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{product}.pdf"'
            return response

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", content_type="text/plain", status=500)