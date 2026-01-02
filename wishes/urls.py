from django.urls import path
from . import views

urlpatterns = [
    path('wishes/', views.wish_list, name='wish_list'),
    path('', views.home, name='home'),
    path('create/', views.wish_create, name='wish_create'),
    path('fulfill/<int:pk>/', views.wish_fulfill, name='wish_fulfill'),
    path('delete/<int:pk>/', views.wish_delete, name='wish_delete'),
    path('explore/', views.explore, name='explore'),
    path('wish/<int:pk>/', views.wish_detail, name='wish_detail'),
]