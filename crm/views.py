from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from smtplib import SMTPAuthenticationError
from django.http import HttpResponse
from django.utils import timezone
from .models import (
    Flight,
    Booking,
    TicketExchange,
    TicketRefund,
    FutureCredit,
    Message,
    generate_pnr
)

from .serializers import (
    FlightSerializer,
    BookingSerializer,
    TicketExchangeSerializer,
    TicketRefundSerializer,
    FutureCreditSerializer,
    MessageSerializer,
    UserSerializer
)


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
            flight_id = data.get('flight')
            flight_obj = None
            calculated_total = 698.98

            if flight_id:
                try:
                    flight_obj = Flight.objects.get(id=flight_id)
                    seats = int(data.get('seats_booked', 1) or 1)
                    calculated_total = flight_obj.price * seats
                except Flight.DoesNotExist:
                    print(f"Warning: Flight ID {flight_id} not found.")

            booking = Booking()
            booking.flight = flight_obj

            if data.get('agent'):
                booking.agent_id = data.get('agent')

            booking.passenger_name = data.get(
                'passenger_name',
                'Rahi Gabani'
            )

            booking.passenger_email = data.get(
                'passenger_email',
                'rahigabani.3@gmail.com'
            )

            booking.seats_booked = int(
                data.get('seats_booked', 1) or 1
            )
            pnr = data.get('pnr_number')

            if not pnr:
                pnr = generate_pnr()

            while Booking.objects.filter(pnr_number=pnr).exists():
                pnr = generate_pnr()

            booking.pnr_number = pnr
            

            booking.status = data.get('status', 'Pending')
            booking.card_holder_name = data.get('card_holder_name') or 'Dynamic Holder'

            raw_card = str(data.get('card_number', '')).strip()

            if raw_card and len(raw_card) >= 4:
                booking.card_number_last4 = raw_card[-4:]
            else:
                booking.card_number_last4 = '7812'

            booking.card_type = data.get('card_type') or 'Visa'
            booking.expiry_date = data.get('expiry_date') or '12/28'
            booking.billing_address = data.get('billing_address') or '138 Sterling Dr Bozeman, MT 59718'

            raw_amount = str(data.get('total_amount', '')).replace('$', '').strip()
            booking.total_amount = raw_amount if raw_amount else calculated_total

            booking.current_step = 3

            booking.airline_name = data.get('airline_name')
            booking.passenger_dob = data.get('passenger_dob')
            booking.departure_city = data.get('departure_city')
            booking.arrival_city = data.get('arrival_city')
            booking.departure_time = data.get('departure_time')
            booking.return_time = data.get('return_time')
            booking.cabin_class = data.get('cabin_class')

            booking.save()
            print(f"DATABASE SUCCESS: Booking Saved dynamically with step={booking.current_step}! ID: {booking.id}")

            email_status = "not_sent"
            email_error = ""

            try:
                passenger_list = [
                    name.strip()
                    for name in booking.passenger_name.split(",")
                    if name.strip()
                ]

                passenger_dobs = [
                    dob.strip()
                    for dob in (booking.passenger_dob or "").split(",")
                    if dob.strip()
                ]

                passengers_data = [
                    (
                        name,
                        passenger_dobs[index] if index < len(passenger_dobs) else ""
                    )
                    for index, name in enumerate(passenger_list)
                ]

                base_url = "http://127.0.0.1:8000"
                auth_link = f"{base_url}/authorize-booking/{booking.id}/"

                html_content = render_to_string(
                    'booking_confirmation.html',
                    {
                        'booking': booking,
                        'passenger_list': passenger_list,
                        'passengers_data': passengers_data,
                        'auth_link': auth_link
                    }
                )

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

            return Response(
                {
                    "message": "Booking Saved Successfully",
                    "status": booking.status,
                    "current_step": booking.current_step,
                    "email_status": email_status,
                    "email_error": email_error,
                    "id": booking.id,
                    "pnr": booking.pnr_number
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as global_err:
            print(f"CRITICAL GLOBAL ERROR: {str(global_err)}")

            return Response(
                {
                    "message": f"Database Error: {str(global_err)}",
                    "status": "Failed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class TicketExchangeViewSet(viewsets.ModelViewSet):
    queryset = TicketExchange.objects.all()
    serializer_class = TicketExchangeSerializer


class TicketRefundViewSet(viewsets.ModelViewSet):
    queryset = TicketRefund.objects.all()
    serializer_class = TicketRefundSerializer


class FutureCreditViewSet(viewsets.ModelViewSet):
    queryset = FutureCredit.objects.all()
    serializer_class = FutureCreditSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')

        if user_id:
            return (
                Message.objects.filter(sender_id=user_id)
                | Message.objects.filter(receiver_id=user_id)
            )

        return Message.objects.all()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


def booking_flight_details_view(request, booking_id=None):
    booking = None

    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)

        if booking.current_step > 1 and request.method == 'GET':
            return redirect(f'/booking/step-{booking.current_step}/{booking.id}/')

    if request.method == 'POST':
        pnr = request.POST.get('pnr_number')
        dep_city = request.POST.get('departure_city')

        if not pnr or not dep_city:
            return render(
                request,
                'flight_booking.html',
                {
                    'error': 'Saari fields bharo!',
                    'booking': booking
                }
            )

        if not booking:
            booking = Booking()

        booking.pnr_number = pnr
        booking.departure_city = dep_city
        booking.current_step = 2
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

    selected_role_clean = str(selected_role).strip().lower()

    user_obj = User.objects.filter(email__iexact=email.strip()).first()

    if not user_obj:
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    user = authenticate(username=user_obj.username, password=password)

    if user is not None:
        actual_role = 'manager' if user.is_staff else 'agent'

        if selected_role_clean != actual_role:
            return Response(
                {
                    'error': f'This account is registered as {actual_role}, not {selected_role}'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(
            {
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'name': user.username,
                    'email': user.email,
                    'role': actual_role
                }
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {'error': 'Invalid email or password'},
        status=status.HTTP_401_UNAUTHORIZED
    )
def authorize_booking_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)

        booking.is_authorized = True
        booking.authorized_at = timezone.now()
        booking.save()

        return HttpResponse("""
        <html>
            <head>
                <title>SkyBook Authorization</title>
            </head>
            <body style="font-family:Arial;text-align:center;padding-top:80px;">
                <h1 style="color:green;">✓ Booking Authorized Successfully</h1>
                <p>You may now close this page.</p>
            </body>
        </html>
        """)

    except Booking.DoesNotExist:
        return HttpResponse(
            "<h2>Invalid Authorization Link</h2>",
            status=404
        )