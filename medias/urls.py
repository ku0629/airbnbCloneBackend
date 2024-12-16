from django.urls import path

from .views import PhotoDetial, GetUploadURL

urlpatterns = [
    path("photos/get-url", GetUploadURL.as_view()),
    path("photo/<int:pk>", PhotoDetial.as_view()),
]
