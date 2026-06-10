<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from smtplib import SMTPAuthenticationError
from .models import Flight, Booking, TicketExchange, TicketRefund, FutureCredit
from .serializers import (FlightSerializer, BookingSerializer, TicketExchangeSerializer, 
                            TicketRefundSerializer, FutureCreditSerializer)
=======
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
    


from .models import Flight, Booking, TicketExchange, TicketRefund, FutureCredit , Message
from .serializers import (
    FlightSerializer,
    BookingSerializer,
    TicketExchangeSerializer,
    TicketRefundSerializer,
    FutureCreditSerializer,
    MessageSerializer,
    UserSerializer
)


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    selected_role = request.data.get('role')

    if not email or not password or not selected_role:
        return Response(
            {'error': 'Email, password and role are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    user = authenticate(username=user_obj.username, password=password)

    if user is not None:
        actual_role = 'manager' if user.is_staff else 'agent'

        if selected_role != actual_role:
            return Response(
                {
                    'error': f'This account is registered as {actual_role}, not {selected_role}'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'role': actual_role
            }
        }, status=status.HTTP_200_OK)

    return Response(
        {'error': 'Invalid email or password'},
        status=status.HTTP_401_UNAUTHORIZED
    )

>>>>>>> 3999f0cc3fb63e0ac6f33cacd02393146848ee55

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

<<<<<<< HEAD
    def create(self, request, *args, **kwargs):
        data = request.data
        print("Incoming raw data from React:", data)

        try:
            # 1. Flight check karo aur total amount nikal lo
            flight_id = data.get('flight')
            flight_obj = None
            calculated_total = 698.98  # Backup price agar flight na mile

            if flight_id:
                try:
                    flight_obj = Flight.objects.get(id=flight_id)
                    seats = int(data.get('seats_booked', 1) or 1)
                    calculated_total = flight_obj.price * seats
                except Flight.DoesNotExist:
                    print(f"Warning: Flight ID {flight_id} not found.")

            # 2. DYNAMIC DATABASE ENTRY (Ek-ek field seedhe React se map hogi)
            booking = Booking()
            booking.flight = flight_obj
            
            # Passenger Details
            booking.passenger_name = data.get('passenger_name', 'Himani Upadhyay')
            booking.passenger_email = data.get('passenger_email', 'himaniupadhyay35@gmail.com')
            booking.pnr_number = data.get('pnr_number', 'SKY999')
            booking.seats_booked = int(data.get('seats_booked', 1) or 1)
            
            # --- CARD DETAILS DYNAMIC FIX START ---
            booking.status = data.get('status', 'Pending')
            booking.card_holder_name = data.get('card_holder_name') or 'Dynamic Holder'
            
            # Card number se spaces/characters saaf karke last 4 digits nikalne ke liye:
            raw_card = str(data.get('card_number', '')).strip()
            if raw_card and len(raw_card) >= 4:
                booking.card_number_last4 = raw_card[-4:]
            else:
                booking.card_number_last4 = '7812' # Fallback default
                
            booking.card_type = data.get('card_type') or 'Visa'
            booking.expiry_date = data.get('expiry_date') or '12/28'
            booking.billing_address = data.get('billing_address') or '138 Sterling Dr Bozeman, MT 59718'
            
            # Total amount se agar $ sign aa raha ho toh use hatane ke liye:
            raw_amount = str(data.get('total_amount', '')).replace('$', '').strip()
            booking.total_amount = raw_amount if raw_amount else calculated_total
            # --- CARD DETAILS DYNAMIC FIX END ---

            # --- SAVE & NEXT STEP TRACKING ---
            # Kyunki step 2 ka saara data submit ho gaya hai, step ko badha kar 3 kar do
            booking.current_step = 3

            # Baaki flight metadata fields
            booking.airline_name = data.get('airline_name')
            booking.passenger_dob = data.get('passenger_dob')
            booking.departure_city = data.get('departure_city')
            booking.arrival_city = data.get('arrival_city')
            booking.departure_time = data.get('departure_time')
            booking.return_time = data.get('return_time')
            booking.cabin_class = data.get('cabin_class')

            booking.save()  # Database mein poora dynamic data save
            print(f"DATABASE SUCCESS: Booking Saved dynamically with step={booking.current_step}! ID: {booking.id}")

            # 3. EMAIL LOGIC
            email_status = "not_sent"
            email_error = ""
            try:
                passenger_list = [name.strip() for name in booking.passenger_name.split(",") if name.strip()]
                passenger_dobs = [dob.strip() for dob in (booking.passenger_dob or "").split(",") if dob.strip()]
                passengers_data = [
                    (name, passenger_dobs[index] if index < len(passenger_dobs) else "")
                    for index, name in enumerate(passenger_list)
                ]
                
                base_url = "http://localhost:5173"
                auth_link = f"{base_url}/authorize-booking/{booking.id}"
                
                html_content = render_to_string('booking_confirmation.html', {
                    'booking': booking,
                    'passenger_list': passenger_list,
                    'passengers_data': passengers_data,
                    'auth_link': auth_link
                })
                
                target_email = booking.passenger_email or settings.EMAIL_HOST_USER
                
                email = EmailMessage(
                    subject=f'SkyBook New Flight Booking Authorization - PNR: {booking.pnr_number}',
                    body=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[target_email]
                )
                email.content_subtype = "html"
                email.send()
                email_status = "sent"
                print("EMAIL SUCCESS: Sent successfully from backend with auth link!")
            except Exception as mail_err:
                email_status = "failed"
                if isinstance(mail_err, SMTPAuthenticationError):
                    email_error = "Gmail rejected the sender login. Use a valid Gmail App Password for EMAIL_HOST_PASSWORD."
                else:
                    email_error = str(mail_err)
                print("EMAIL ERROR: Template parsing or SMTP failed. Reason:", str(mail_err))

            # React ko exact dynamic data aur current_step return karo response mein
            return Response({
                "message": "Booking Saved Successfully",
                "status": booking.status,
                "current_step": booking.current_step,
                "email_status": email_status,
                "email_error": email_error,
                "id": booking.id,
                "pnr": booking.pnr_number
            }, status=status.HTTP_201_CREATED)

        except Exception as global_err:
            print(f"CRITICAL GLOBAL ERROR: {str(global_err)}")
            return Response({
                "message": f"Database Error: {str(global_err)}", 
                "status": "Failed"
            }, status=status.HTTP_400_BAD_REQUEST)
        
=======

>>>>>>> 3999f0cc3fb63e0ac6f33cacd02393146848ee55
class TicketExchangeViewSet(viewsets.ModelViewSet):
    queryset = TicketExchange.objects.all()
    serializer_class = TicketExchangeSerializer


class TicketRefundViewSet(viewsets.ModelViewSet):
    queryset = TicketRefund.objects.all()
    serializer_class = TicketRefundSerializer


class FutureCreditViewSet(viewsets.ModelViewSet):
    queryset = FutureCredit.objects.all()
    serializer_class = FutureCreditSerializer

<<<<<<< HEAD
def booking_flight_details_view(request, booking_id=None):
    booking = None
    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)
        # Resume Logic: Agar user step 1 par wapis aaye aur pehle se step 2 save ho
        if booking.current_step > 1 and request.method == 'GET':
            return redirect(f'/booking/step-{booking.current_step}/{booking.id}/')

    if request.method == 'POST':
        pnr = request.POST.get('pnr_number')
        dep_city = request.POST.get('departure_city')

        if not pnr or not dep_city:
            return render(request, 'flight_booking.html', {'error': 'Saari fields bharo!', 'booking': booking})

        if not booking: booking = Booking()
        booking.pnr_number = pnr
        booking.departure_city = dep_city
        booking.current_step = 2  # Agla step lock kar diya
        booking.save()

        return redirect(f'/booking/step-2/{booking.id}/')

    return render(request, 'flight_booking.html', {'booking': booking})

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    selected_role = request.data.get('role')

    if not email or not password or not selected_role:
        return Response(
            {'error': 'Email, password and role are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Clean the role string to avoid capital/small letter mismatches
    selected_role_clean = str(selected_role).strip().lower()

    # Purane try-except ko hata kar bas yeh 2 lines likh do
    user_obj = User.objects.filter(email__iexact=email.strip()).first()
    if not user_obj:
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    user = authenticate(username=user_obj.username, password=password)

    if user is not None:
        # Django staff status check karke role decide karega
        actual_role = 'manager' if user.is_staff else 'agent'

        if selected_role_clean != actual_role:
            return Response(
                {
                    'error': f'This account is registered as {actual_role}, not {selected_role}'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'role': actual_role
            }
        }, status=status.HTTP_200_OK)

    return Response(
        {'error': 'Invalid email or password'},
        status=status.HTTP_401_UNAUTHORIZED
    )
=======
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')

        if user_id:
            return Message.objects.filter(
                sender_id=user_id
            ) | Message.objects.filter(
                receiver_id=user_id
            )

        return Message.objects.all()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
>>>>>>> 3999f0cc3fb63e0ac6f33cacd02393146848ee55
