# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AnonymousResponse

def anonymous_response_create(request):
    if request.method == "POST":
        # Extract data from POST
        phone_number = request.POST.get("phone_number")
        message_text = request.POST.get("message")
        
        # Optionally, you can add your own validation here
        if message_text:  # Let's assume message is required
            # Create and save the instance
            response_instance = AnonymousResponse(phone_number=phone_number, message=message_text)
            response_instance.save()
            messages.success(request, "Your report has been submitted successfully.")
            return redirect('home')  # Redirect to homepage or another URL
        else:
            messages.error(request, "Please provide a message.")
    
    return render(request, "index.html")

def homepage(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact_us.html')

def responders(request):
    return render(request,'responders.html')
