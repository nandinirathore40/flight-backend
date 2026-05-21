from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (FlightViewSet, BookingViewSet, TicketExchangeViewSet, 
                    TicketRefundViewSet, FutureCreditViewSet)

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'exchanges', TicketExchangeViewSet)
router.register(r'refunds', TicketRefundViewSet)
router.register(r'future-credits', FutureCreditViewSet) # Naya rasta joda

urlpatterns = [
    path('', include(router.urls)),
]