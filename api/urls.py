from django.urls import path

from . import views

urlpatterns = [
    path('ads/new/', views.AdCreateAPIView.as_view(), name='ad-create'),
    path('ads/', views.AdListAPIView.as_view(), name='ad-list'),
    path('ads/<int:pk>/', views.AdDetailAPIView.as_view(), name='ad-detail'),

    path('comments/new/', views.CommentCreateAPIView.as_view(), name='comment-create'),
]