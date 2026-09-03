from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='Index'),
    path('suggestions/',views.suggestions,name='suggestions'),
    path('book/',views.book_detail,name='book_detail'),
    path('searched/', views.book_search,name='book_search')
]
