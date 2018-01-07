from django.contrib import admin
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'issue_date', 'issue_time', 'fine_amount']

# Register your models here.
admin.site.register(Ticket, TicketAdmin)