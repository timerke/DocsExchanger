from django.contrib import admin
from django.urls import path, re_path
from app import views

urlpatterns = [
    re_path(r'about/', views.about, name='about'),
    path(r'downloal_file', views.download_file, name='download_file'),
    path(r'estimate_file', views.estimate_file, name='estimate_file'),
    re_path(r'private/auth', views.sign_in, name='sign_in'),
    re_path(r'private/delete_file', views.delete_file, name='delete_file'),
    re_path(r'private/exit', views.exit, name='exit'),
    re_path(r'private/save_file', views.save_file, name='save_file'),
    re_path(r'private/start', views.private_start, name='private_start'),
    re_path(r'private/upload_file', views.upload_file, name='upload_file'),
    re_path(r'private/', views.private, name='private'),
    re_path(r'', views.index, name='home'),
    path('admin/', admin.site.urls),
]
