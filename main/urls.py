from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('create_post/', views.create_post, name='createpost'),
    path('user_dashboard/', views.show_dashboard, name='userdashboard'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),

]
