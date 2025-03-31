from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('session_list/', views.session_list, name='session_list'),
    path('create/', views.session_create, name='session_create'),
    path('update/<int:pk>/', views.session_update, name='session_update'),
    path('delete/<int:pk>/', views.session_delete, name='session_delete'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('guided-meditations/', views.guided_meditation_list, name='guided_meditation_list'),
    path('guided-meditations/<int:pk>/', views.guided_meditation_detail, name='guided_meditation_detail'),

    path('save_meditation/', views.save_meditation_session, name='save_meditation'),
    path('add-session/', views.add_session, name='add_session'),
    path("profile/", views.profile_page, name="profile"),
    path("delete-account/", views.delete_account, name="delete_account"),
]