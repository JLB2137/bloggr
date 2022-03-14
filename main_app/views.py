from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Post

# Create your views here.

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


# ++++++++++++++++++++++++++++++

def post_list(request):
    posts = Post.published.all()
    return render(request,'post_list.html',{'posts':posts})

def post_detail(request, post):
    post=get_object_or_404(Post,slug=post,status='published')
    return render(request, 'post_detail.html',{'post':post})