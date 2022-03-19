from django.urls import path
from . import views

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
]