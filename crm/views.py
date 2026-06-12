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
