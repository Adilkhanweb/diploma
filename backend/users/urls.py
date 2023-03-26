from django.urls import path

from account import views

app_name = "account"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signout/", views.signout, name="signout"),
    path('profile/<int:user_profile_id>', views.profile, name='profile'),
]
