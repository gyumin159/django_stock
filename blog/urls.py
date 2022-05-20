from django.urls import path
from .views import BlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView
from . import views

urlpatterns = [
    path('', BlogListView.as_view(), name='blog-home'),
    path('newpost/', BlogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='blog-update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
    path('search/', views.search_func, name='blog-search'),
]