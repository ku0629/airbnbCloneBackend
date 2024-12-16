from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("sign-up", views.SignUp.as_view()),
    path("log-in", views.LogIn.as_view()),  # Login with Cookies
    path("log-out", views.LogOut.as_view()),
    path("token-login", obtain_auth_token),  # Login with Token
    path("jwt-login", views.JWTLogIn.as_view()),  # Login with JWT
    path("github", views.GithubLogIn.as_view()),
    path("kakao", views.KakaoLogIn.as_view()),
    path("bookings", views.MyBookings.as_view()),
    path("bookings/<int:pk>/cancel", views.CancelMyBooking.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
]
