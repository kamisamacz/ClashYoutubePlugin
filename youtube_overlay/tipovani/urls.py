from django.urls import path
from . import views

app_name = "tipovani"

urlpatterns = [
    path("create/<int:event_id>/", views.create_kolo, name="create_kolo"),
    path("uzavrit/<int:kolo_id>/", views.uzavrit_kolo, name="uzavrit_kolo"),
    path("event/<int:event_id>/", views.user_tipovani, name="user_tipovani"),
    path("kolo/<int:kolo_id>/", views.kolo_detail, name="kolo_detail"),
    path("kolo/<int:kolo_id>/otevrit/", views.otevrit_kolo, name="otevrit_kolo"),
    path('vyhodnotit_kolo/<int:kolo_id>/<str:team>/', views.vyhodnotit_kolo, name="vyhodnotit_kolo"),
]
