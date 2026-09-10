from django.contrib import admin
from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('activate/<uidb64>/<token>',views.activate,name="activate"),
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path(
        'password_change',
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy('index'),
            template_name='users/password_change.html',
            ),
        name='password_change'
        ),
    path('change_username',views.username_change,name='change_username'),
    path('delete/',views.delete,name='delete')
]
