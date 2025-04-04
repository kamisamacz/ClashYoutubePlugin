from django.urls import path
from .views import overlay_view, get_overlay_content, update_overlay

app_name = "overlay"

urlpatterns = [
    path("", overlay_view, name="overlay"),
    path("get/", get_overlay_content, name="get_overlay"),
    path("update/<int:event_id>/", update_overlay, name="update_overlay"),
]
