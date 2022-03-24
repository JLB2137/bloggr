from django.urls import path
from . import views
from .views import AddPostView, UpdatePostView, PostDeleteView

app_name = 'main_app'

urlpatterns = [
    
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logoutUser, name='logout'),
    
 

    path('',views.post_list,name="post_list"),
    path('<slug:post>/',views.post_detail,name="post_detail"),
    path('comment/reply/', views.reply_page, name="reply"),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_tag'),

    path('posts/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),


    path('post/create/', AddPostView.as_view(), name='post_create'),
    path('posts/update/<int:pk>/', UpdatePostView.as_view(), name='post_update'),
    # path('posts/delete/<int:pk>/', DeletePostView.as_view(), name='post_delete'),
   
]
