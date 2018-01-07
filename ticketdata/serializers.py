from django.contrib.auth.models import User, Group
from rest_framework import serializers

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
