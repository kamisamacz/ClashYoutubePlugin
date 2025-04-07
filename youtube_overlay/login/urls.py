from django.urls import path
from .views import login_view, dashboard_view, logout_view

app_name = "login"  # ✅ Namespace pro správné reverzní URL

urlpatterns = [
    path("", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),  # ✅ Musí existovat
    path("logout/", logout_view, name="logout"),
]
