from django.db import models

class Ticket(models.Model):
    ticket_number = models.IntegerField()
    issue_date = models.DateField()
    issue_time = models.TimeField()
    rp_state_plate = models.CharField(max_length=2, null=True)
    make = models.CharField(max_length=4, null=True)
    body_style = models.CharField(max_length=2, null=True)
    color = models.CharField(max_length=2, null=True)
    agency = models.SmallIntegerField(default=-1, null=True)
    violation_description = models.CharField(max_length=50, null=True)
    fine_amount = models.FloatField(default=0.0, null=True)
    latitude = models.FloatField(default=0.0, null=True)
    longitude = models.FloatField(default=0.0, null=True)
