from rest_framework import viewsets
from .models import Flight, Booking, TicketExchange, TicketRefund, FutureCredit
from .serializers import (FlightSerializer, BookingSerializer, TicketExchangeSerializer, 
                            TicketRefundSerializer, FutureCreditSerializer)

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class TicketExchangeViewSet(viewsets.ModelViewSet):
    queryset = TicketExchange.objects.all()
    serializer_class = TicketExchangeSerializer

class TicketRefundViewSet(viewsets.ModelViewSet):
    queryset = TicketRefund.objects.all()
    serializer_class = TicketRefundSerializer

class FutureCreditViewSet(viewsets.ModelViewSet):
    queryset = FutureCredit.objects.all()
    serializer_class = FutureCreditSerializer