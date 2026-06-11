from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import login_view

router = DefaultRouter(trailing_slash=True)

router.register(r'flights', views.FlightViewSet, basename='flights')
router.register(r'bookings', views.BookingViewSet, basename='bookings')

router.register(r'exchanges', views.TicketExchangeViewSet, basename='exchanges')
router.register(r'refunds', views.TicketRefundViewSet, basename='refunds')

router.register(r'ticket-exchanges', views.TicketExchangeViewSet, basename='ticket-exchanges')
router.register(r'ticket-refunds', views.TicketRefundViewSet, basename='ticket-refunds')

router.register(r'future-credits', views.FutureCreditViewSet, basename='future-credits')
router.register(r'messages', views.MessageViewSet, basename='messages')
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),

    path('api/', include(router.urls)),
    path('api/login/', login_view, name='api_login'),

    path('booking/step-1/', views.booking_flight_details_view, name='step_1'),
    path('booking/step-1/<int:booking_id>/', views.booking_flight_details_view, name='step_1_resume'),
    path(
    'authorize-booking/<int:booking_id>/',
    views.authorize_booking_view,
    name='authorize_booking'
),
]