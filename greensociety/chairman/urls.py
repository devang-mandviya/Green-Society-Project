"""greensociety URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chairman import views

urlpatterns = [
    path('', views.home, name='home'),
    path('m-index/', views.home, name='m-index'),
    path('login/', views.login, name='login'),
    path('change-password/', views.change_password, name='change-password'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('logout/', views.logout, name='logout'),
    path('add-member/', views.add_member, name='add-member'),
    path('all-member/', views.all_member, name='all-member'),
    path('m-all-member/', views.all_member, name='m-all-member'),
    path('my-profile', views.my_profile, name='my-profile'),
    path('m-my-profile', views.my_profile, name='m-my-profile'),
    path('add-notice/', views.add_notice, name='add-notice'),
    path('m-add-notice/', views.add_notice, name='m-add-notice'),
    path('all-notice/', views.all_notice, name='all-notice'),
    path('m-all-notice/', views.all_notice, name='m-all-notice'),
    path('add-event/', views.add_event, name='add-event'),
    path('m-add-event/', views.add_event, name='m-add-event'),
    path('all-event/', views.all_event, name='all-event'),
    path('specific-user/<int:pk>', views.specific_user, name='specific-user'),
    path('m-specific-user/<int:pk>', views.specific_user, name='m-specific-user'),
    path('delete-user/<int:pk>', views.delete_user, name='delete-user'),
    path('delete-notice/<int:pk>', views.delete_notice, name='delete-notice'),
    path('delete-event/<int:pk>', views.delete_event, name='delete-event'),
    path('change-password-o/',views.change_password_o,name='change-password-o'),
    path('contact-list/',views.contact_list,name='contact-list'),
    path('m-contact-list/',views.contact_list,name='m-contact-list'),
    path('post/', views.post, name='post'),
    path('m-post/', views.post, name='m-post'),
    path('add-maintainance/', views.add_maintainance, name='add-maintainance'),
    path('all-maintainance/', views.all_maintainance, name='all-maintainance'),
    path('m-all-maintainance/', views.m_all_maintainance, name='m-all-maintainance'),
]
