from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel ka rasta
    path('admin/', admin.site.urls),  
    
    # 🎯 YAHAN SE 'api/' HATA DIYA HAI:
    # Kyunki 'api/' humne niche wali crm/urls.py mein lagaya hua hai
    path('', include('crm.urls')), 
     
]