from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="reviewer/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("submit/", views.submit_code_view, name="submit_code"),
    path("review/<int:pk>/", views.review_detail_view, name="review_detail"),
    path("history/", views.review_history_view, name="review_history"),
]
