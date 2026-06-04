from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FlightViewSet,
    BookingViewSet,
    TicketExchangeViewSet,
    TicketRefundViewSet,
    FutureCreditViewSet,
    MessageViewSet,
    login_view,
    UserViewSet
)

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'exchanges', TicketExchangeViewSet)
router.register(r'refunds', TicketRefundViewSet)
router.register(r'future-credits', FutureCreditViewSet)
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', include(router.urls)),
]