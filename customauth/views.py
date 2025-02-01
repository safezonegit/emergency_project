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
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            
            return render(request,'registration/registration.html',{'form':form})
    else:
        form = UserRegistrationForm()
    return render(request,'registration/registration.html',{'form':form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to homepage
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "registration/login.html")

