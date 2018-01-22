from django.contrib.auth.models import User, Group
from rest_framework import serializers

from . import DateCount, DayStats, MonthStats
from ticketdata.models import Ticket

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = ('ticket_number', 'issue_date', 'issue_time', 'rp_state_plate', 'make', 'body_style', 'color', 'agency', 'violation_description', 'fine_amount', 'latitude', 'longitude')

class DateCountSerializer(serializers.Serializer):
    date = serializers.DateTimeField(format="%Y-%m-%d")
    count = serializers.IntegerField()

    def create(self, validated_data):
        return DateCount(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance

class DayStatsSerializer(serializers.Serializer):
    day = serializers.IntegerField()
    avg = serializers.FloatField()
    std = serializers.FloatField()
    
    def create(self, validated_data):
        return DayStats(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance

class MonthStatsSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    avg = serializers.FloatField()
    std = serializers.FloatField()
    
    def create(self, validated_data):
        return MonthStats(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance