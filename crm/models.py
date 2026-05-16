from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField(default=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.flight_number

class Booking(models.Model):  # <--- Ye class honi zaroori hai
    passenger_name = models.CharField(max_length=200)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Confirmed')

    def __str__(self):
        return f"{self.passenger_name} - {self.flight.flight_number}"