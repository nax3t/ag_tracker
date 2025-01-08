from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegistrationForm  # Import our custom form

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  # Use our custom form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()  # Use our custom form
    return render(request, 'registration/register.html', {'form': form}) 