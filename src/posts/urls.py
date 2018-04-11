
from django.urls import path
from django.conf.urls import url
from . import views


app_name= "posts"
urlpatterns = [
    path('', views.post_list, name="list"),
    path('create/', views.post_create, name="post_create"),
    path('<str:slug>/', views.post_detail, name="detail"),
    path('<str:slug>/edit/', views.post_update, name="update"),
    path('<str:slug>/delete/', views.post_delete, name="delete"),
]
