from rest_framework import serializers
from .models import Flight, Booking, TicketExchange, TicketRefund, FutureCredit

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class TicketExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketExchange
        fields = '__all__'

class TicketRefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketRefund
        fields = '__all__'

class FutureCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureCredit
        fields = '__all__'