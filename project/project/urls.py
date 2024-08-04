from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('taks/', include('taks.urls')),  # Inclui as URLs do app tasks
]
