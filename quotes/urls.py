from django.urls import path
from . import views

urlpatterns = [
    path('', views.quote_list, name='home'),
    path('author/<int:author_id>/', views.author_detail, name='author'),
    path('add-author/', views.add_author, name='add_author'),
    path('add-quote/', views.add_quote, name='add_quote'),
    path('tag/<str:tag_name>/', views.quotes_by_tag, name='tag'),
    path('register/', views.register, name='register'),
]
