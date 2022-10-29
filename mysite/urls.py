from django.contrib import admin
from django.urls import path, include

from app.views import handler_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]

handler404 = "app.views.handler_404"
