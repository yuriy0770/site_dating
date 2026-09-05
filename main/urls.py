from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.user_list, name='user_list'),
    path('users/men/', views.user_list_men, name='user_list_men'),
    path('users/women/', views.user_list_women, name='user_list_women'),
    path('user/<slug:slug>/', views.user_detail, name='user_detail'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('like/<int:user_id>/', views.like_user, name='like_user'),
    path('user/id/<int:user_id>/', views.user_detail_by_id, name='user_detail_by_id'),
    path('chats/', views.chat_list, name='chat_list'),
    path('chat/<int:room_id>/', views.chat_detail, name='chat_detail'),
]
