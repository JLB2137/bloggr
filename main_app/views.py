from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid signup'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message,}
    return render(request, 'registration/signup.html',context)

def profile(request):
    return render(request, 'profile.html')