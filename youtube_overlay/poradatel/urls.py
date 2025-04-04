from django.urls import path
from .views import event_list, join_event, leave_event, event_management, manage_event, event_highscore

app_name = "poradatel"  # 🚀 Přidáváme namespace

urlpatterns = [
    path("", event_list, name="event_list"),
    path("join/<int:event_id>/", join_event, name="join_event"),
    path("leave/<int:event_id>/", leave_event, name="leave_event"),
    path("manage/", event_management, name="event_management"),
    path("manage/<int:event_id>/", manage_event, name="manage_event"),  # ✅ Přidáno správné URL
    path('manage/<int:event_id>/highscore/', event_highscore, name='event_highscore'),
]
