from django.urls import path

from . import views

urlpatterns = [
    path("ads/new/", views.AdCreateAPIView.as_view(), name="ad-create"),
    path("ads/", views.AdListAPIView.as_view(), name="ad-list"),
    path("ads/update/<int:pk>/", views.AdUpdateAPIView.as_view(), name="ad-update"),
    path(
        "ads/detail/<int:pk>/", views.AdDetailDestroyAPIView.as_view(), name="ad-detail"
    ),
    path(
        "ads/delete/<int:pk>/", views.AdDetailDestroyAPIView.as_view(), name="ad-delete"
    ),
    path("comments/new/", views.CommentCreateAPIView.as_view(), name="comment-create"),
]
