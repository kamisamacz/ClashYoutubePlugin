from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("overlay/", include("overlay.urls")),  # Pokud má overlay vlastní URL
    path("", include("login.urls")),  # 🚀 Přesměrování na login aplikaci
    path("poradatel/", include("poradatel.urls")),  # Pořadatel sekce
    path("tipovani/", include("tipovani.urls")),
]
