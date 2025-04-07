from django.urls import path
from . import views
from .views import kola_tipovani_api
from .views import otevrena_kola_json

app_name = "tipovani"

urlpatterns = [
    path("create/<int:event_id>/", views.create_kolo, name="create_kolo"),
    path("uzavrit/<int:kolo_id>/", views.uzavrit_kolo, name="uzavrit_kolo"),
    path("event/<int:event_id>/", views.user_tipovani, name="user_tipovani"),
    path("kolo/<int:kolo_id>/", views.kolo_detail, name="kolo_detail"),
    path("kolo/<int:kolo_id>/otevrit/", views.otevrit_kolo, name="otevrit_kolo"),
    path('vyhodnotit_kolo/<int:kolo_id>/<str:team>/', views.vyhodnotit_kolo, name="vyhodnotit_kolo"),
    path("api/kola_tipovani/<int:event_id>/", kola_tipovani_api, name="kola_tipovani_api"),
    path('api/otevrena_kola/<int:event_id>/', otevrena_kola_json, name='otevrena_kola_json'),
]
