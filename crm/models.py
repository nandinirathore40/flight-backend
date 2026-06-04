from django.db import models
from django.contrib.auth.models import User
import uuid


class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField(default=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number} ({self.origin} -> {self.destination})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    agent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    pnr_number = models.CharField(
        max_length=10,
        unique=True,
        default=uuid.uuid4().hex[:8].upper()
    )
    passenger_name = models.CharField(max_length=200)
    passenger_email = models.EmailField(null=True, blank=True)
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    seats_booked = models.IntegerField(default=1)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.pnr_number} - {self.passenger_name}"


class TicketExchange(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    old_ticket_number = models.CharField(max_length=50)
    airline_name = models.CharField(max_length=100)
    pnr_number = models.CharField(max_length=10)
    exchange_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    new_departure_city = models.CharField(max_length=100)
    new_arrival_city = models.CharField(max_length=100)
    new_departure_date = models.DateField()
    new_return_date = models.DateField(null=True, blank=True)
    exchange_reason = models.TextField()
    exchange_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exchange for {self.pnr_number} - Fee: ${self.exchange_fee}"


class TicketRefund(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    ticket_number = models.CharField(max_length=50)
    airline_name = models.CharField(max_length=100)
    pnr_number = models.CharField(max_length=10)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_status = models.CharField(max_length=50)
    refund_method = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=200)
    refund_reason = models.TextField()
    internal_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund for {self.customer_name} - PNR: {self.pnr_number}"


class FutureCredit(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    original_ticket_number = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=200)
    airline_name = models.CharField(max_length=100)
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    customer_email = models.EmailField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Credit for {self.customer_name} - ${self.credit_amount}"

from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}'