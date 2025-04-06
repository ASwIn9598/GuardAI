from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name='home'),
    path('history/', views.history, name='history'),


    path("", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.signout, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path('check_detection/', views.check_detection, name='check_detection'),
    path('reset_detection/', views.reset_detection, name='reset_detection'),

    path('control_detection/', views.control_detection, name='control_detection'),
    # path('video_feed/', views.video_feed, name='video_feed'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)