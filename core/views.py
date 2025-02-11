from django.shortcuts import render

# Create your views here.

def homepage(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact_us.html')

def responders(request):
    return render(request,'responders.html')
