from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')  # Redirect to login page
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/registration.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to homepage
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "registration/login.html")

