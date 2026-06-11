from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("api/sheets/<str:sheet_name>/", views.sheet_values, name="sheet_values"),
]
