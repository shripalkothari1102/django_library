from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    # AUTHOR URLS
    path('author_list/', views.AuthorListView.as_view(), name='author_list'),
    path('author_detail/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
    path('author_create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('author_update/<int:pk>', views.AuthorUpdateView.as_view(), name='author_update'),

    # PUBLISHER URLS
    path('publisher_list/', views.PublisherListView.as_view(), name='publisher_list'),
    path('publisher_detail/<int:pk>', views.PublisherDetailView.as_view(), name='publisher_detail'),
    path('publisher_create/', views.PublisherCreateView.as_view(), name='publisher_create'),
    path('publisher_update/<int:pk>', views.PublisherUpdateView.as_view(), name='publisher_update'),

    # BOOK URLS
    path('book_list/', views.BookListView.as_view(), name='book_list'),
    path('book_detail/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('book_create/', views.BookCreateView.as_view(), name='book_create'),
    path('book_update/<int:pk>', views.BookUpdateView.as_view(), name='book_update'),
    path('book_publish/<int:pk>', views.BookPublishView.as_view(), name='book_publish'),
]