from django.shortcuts import render,redirect
from .forms import *
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            
            return render(request,'user_register.html',{'form':form})
    else:
        form = UserRegistrationForm()
    return render(request,'user_register.html',{'form':form})