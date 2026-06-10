from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from . import views 
from .views import login_view

router = DefaultRouter(trailing_slash=True)
router.register(r'flights', views.FlightViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'ticket-exchanges', views.TicketExchangeViewSet)
router.register(r'ticket-refunds', views.TicketRefundViewSet)
router.register(r'future-credits', views.FutureCreditViewSet)

urlpatterns = [
    # ---- 🅰️ REACT API PATHS ----
    # Isse ab exact 'api/bookings/' ka raasta banega
    path('api/', include(router.urls)),
    path('api/login/', login_view, name='login'),
    # Backup path just in case React strict POST request maare
    path('api/bookings/', views.BookingViewSet.as_view({'post': 'create', 'get': 'list'})),

    # ---- 🅱️ HTML FORM PATHS ----
    path('booking/step-1/', views.booking_flight_details_view, name='step_1'),
    path('booking/step-1/<int:booking_id>/', views.booking_flight_details_view, name='step_1_resume'),

=======

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
>>>>>>> 3999f0cc3fb63e0ac6f33cacd02393146848ee55
]