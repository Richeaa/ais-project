from django.shortcuts import render
from .form import productForm

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

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