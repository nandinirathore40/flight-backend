from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # <--- Ye 'urls' hona chahiye, 'view_s' nahi
    path('api/', include('crm.urls')),
]