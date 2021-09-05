from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('wall', views.wall),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('makepost', views.makepost),
    path('comment', views.comment),
    path('delete/<nam>', views.delete),
    path( 'deletecomment/<nom>', views.deletecomment),
    path('edit/<nam>', views.edit),
]
