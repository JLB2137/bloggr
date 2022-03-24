from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Photo
from .forms import CommentForm, CustomUserCreationForm, CustomUserCreationForm2
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from django.contrib import messages

import uuid
import boto3

from django.contrib.auth import logout


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'bloggr-phoenix'

# Create your views here.

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'about.html')

def add_photo(request, post_id):
    
    photo_file = request.FILES.get('photo-file')
    
    
    if photo_file:
        
        s3 = boto3.client('s3')
        
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
       
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            
            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            photo = Photo(url=url, post_id=post_id)
            
            photo.save()
            
        except Exception as error:
            print('*************************')
            print('An error occurred while uploading to S3')
            print(error)
            print('*************************')
            
        
    return redirect('main_app:post_detail', post_id=post_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = list(form.errors.get_json_data().values())[0][0]['message']
    form = CustomUserCreationForm()
    context = {'form': form, 'error_message': error_message,}
    return render(request, 'registration/signup.html',context)

def profile(request):
    return render(request, 'profile.html')


def logoutUser(request):
    logout(request)
    template = 'base.html'
    return render(request, template)




# ++++++++++++++++++++++++++++++

def post_list(request, tag_slug=None):
    posts = Post.published.all()

    # post tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    # search
    query = request.GET.get("q")
    if query:
        posts=Post.published.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()

    
    return render(request,'post_list.html',{'posts':posts})

def post_detail(request, post):
    post=get_object_or_404(Post,slug=post,status='published')
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            # redirect to same page and focus on that comment
            return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()

     # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:6]
    return render(request, 'post_detail.html',{'post':post,'comments': comments,'comment_form':comment_form,'similar_posts':similar_posts})
    


# handling reply, reply view
def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input

            reply = form.save(commit=False)
    
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url+'#'+str(reply.id))

    return redirect("/")


class AddPostView(CreateView):
    model = Post
    template_name = "main_app/post_form.html"
    fields = '__all__'

class UpdatePostView(UpdateView):
    model = Post
    template_name = "main_app/update_post.html"
    fields = '__all__'


class PostDeleteView(DeleteView):
    model = Post
    template_name = "main_app/post_confirm_delete.html"
    success_url = reverse_lazy('main_app:post_list')
