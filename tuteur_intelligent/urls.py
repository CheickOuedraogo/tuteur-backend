"""
URL configuration for tuteur_intelligent project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.http import JsonResponse

def home_view(request):
    return JsonResponse({"message": "Backend Faso Tuteur est en ligne ! 🚀", "status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', home_view), # Route pour la racine /
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
