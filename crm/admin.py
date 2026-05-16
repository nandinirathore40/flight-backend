from django.contrib import admin
from .models import Flight, Booking

# In dono models ko admin panel mein register kar rahe hain
admin.site.register(Flight)
admin.site.register(Booking)