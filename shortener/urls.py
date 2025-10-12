from django.urls import path
from . import views

app_name = "shortener"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.dashboard, name="dashboard"),
    path('<str:short_code>/', views.redirect_view, name='redirect'),
    path("delete/<int:pk>/", views.delete_url, name="delete"),
]
