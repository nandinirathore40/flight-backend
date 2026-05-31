from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Flight, Booking, TicketExchange, TicketRefund, FutureCredit
from .serializers import (FlightSerializer, BookingSerializer, TicketExchangeSerializer, 
                            TicketRefundSerializer, FutureCreditSerializer)

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        print("Incoming raw data from React:", data)

        try:
            # 1. Pehle flight_id check karo aur object fetch karo taaki NOT NULL error na aaye
            flight_id = data.get('flight')
            flight_obj = None
            calculated_total = 698.98  # Backup price

            if flight_id:
                try:
                    flight_obj = Flight.objects.get(id=flight_id)
                    seats = int(data.get('seats_booked', 1) or 1)
                    calculated_total = flight_obj.price * seats
                    print(f"Flight Found! ID: {flight_obj.id}, Total: {calculated_total}")
                except Flight.DoesNotExist:
                    print(f"Warning: Flight ID {flight_id} not found in Database.")

            # 2. Sahi tarike se direct object ke sath Booking entry banao
            booking = Booking.objects.create(
                flight=flight_obj,  # Yeh direct flight map karega, error nahi aayega!
                passenger_name=data.get('passenger_name', 'Himani Upadhyay'),
                passenger_email=data.get('passenger_email', 'himaniupadhyay35@gmail.com'),
                pnr_number=data.get('pnr_number', data.get('pnr_number', 'SKY999')),
                seats_booked=int(data.get('seats_booked', 1) or 1),
                status='Confirmed',
                total_amount=calculated_total
            )
            
            print(f"🔥 DATABASE SUCCESS: Booking Saved! ID: {booking.id}")

            # 3. DIRECT PERMANENT EMAIL LOGIC
            try:
                html_content = render_to_string('booking_confirmation.html', {'booking': booking})
                target_email = booking.passenger_email or 'skybookcrm@gmail.com'
                
                email = EmailMessage(
                    subject=f'SkyBook New Flight Booking Authorization - PNR: {booking.pnr_number}',
                    body=html_content,
                    from_email='skybookcrm@gmail.com',
                    to=[target_email]
                )
                email.content_subtype = "html"
                email.send()
                print("🏆 EMAIL SUCCESS: Email triggered from backend successfully!")
            except Exception as mail_err:
                print("❌ EMAIL ERROR: Email sending failed! Reason:", str(mail_err))

            return Response({
                "message": "Booking Saved Successfully",
                "status": "Confirmed",
                "id": booking.id
            }, status=status.HTTP_201_CREATED)

        except Exception as global_err:
            print(f"❌ CRITICAL GLOBAL ERROR: {str(global_err)}")
            return Response({
                "message": "Database/Validation Error occurred", 
                "status": "Failed"
            }, status=status.HTTP_400_BAD_REQUEST)

class TicketExchangeViewSet(viewsets.ModelViewSet):
    queryset = TicketExchange.objects.all()
    serializer_class = TicketExchangeSerializer

class TicketRefundViewSet(viewsets.ModelViewSet):
    queryset = TicketRefund.objects.all()
    serializer_class = TicketRefundSerializer

class FutureCreditViewSet(viewsets.ModelViewSet):
    queryset = FutureCredit.objects.all()
    serializer_class = FutureCreditSerializer