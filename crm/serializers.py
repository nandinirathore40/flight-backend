from rest_framework import serializers
from .models import (
    Flight,
    Booking,
    TicketExchange,
    TicketRefund,
    FutureCredit,
    Message
)
from django.contrib.auth.models import User

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(
        source='agent.username',
        read_only=True
    )

    agent_email = serializers.CharField(
        source='agent.email',
        read_only=True
    )

    agent_role = serializers.SerializerMethodField()

    def get_agent_role(self, obj):
        if obj.agent and obj.agent.is_staff:
            return "Admin"
        return "Agent"

    class Meta:
        model = Booking
        fields = '__all__'


class TicketExchangeSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(
        source='agent.username',
        read_only=True
    )

    agent_email = serializers.CharField(
        source='agent.email',
        read_only=True
    )

    agent_role = serializers.SerializerMethodField()

    def get_agent_role(self, obj):
        if obj.agent and obj.agent.is_staff:
            return "Admin"
        return "Agent"

    class Meta:
        model = TicketExchange
        fields = '__all__'


class TicketRefundSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(
        source='agent.username',
        read_only=True
    )

    agent_email = serializers.CharField(
        source='agent.email',
        read_only=True
    )

    agent_role = serializers.SerializerMethodField()

    def get_agent_role(self, obj):
        if obj.agent and obj.agent.is_staff:
            return "Admin"
        return "Agent"

    class Meta:
        model = TicketRefund
        fields = '__all__'


class FutureCreditSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(
        source='agent.username',
        read_only=True
    )

    agent_email = serializers.CharField(
        source='agent.email',
        read_only=True
    )

    agent_role = serializers.SerializerMethodField()

    def get_agent_role(self, obj):
        if obj.agent and obj.agent.is_staff:
            return "Admin"
        return "Agent"

    class Meta:
        model = FutureCredit
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    receiver_name = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

    def get_role(self, obj):
        return 'manager' if obj.is_staff else 'agent'