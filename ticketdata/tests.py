import time

from django.test import TestCase

from ticketdata.models import Ticket

class TicketModelTestCase(TestCase):
    def setUp(self):
        self.data = [
            {"ticket_number":1001235874,"issue_date":self.helper_to_date("2015-08-22"),"issue_time":self.helper_to_time("10:55:00"),"rp_state_plate":"CA","make":"PORS","body_style":"PA","color":"SI","agency":1,"violation_description":"NO EVIDENCE OF REG","fine_amount":50.0,"latitude":99999.0,"longitude":99999.0},
            {"ticket_number":1001235885,"issue_date":self.helper_to_date("2015-08-24"),"issue_time":self.helper_to_time("08:30:00"),"rp_state_plate":"CA","make":"NISS","body_style":"PA","color":"TN","agency":1,"violation_description":"NO EVIDENCE OF REG","fine_amount":50.0,"latitude":99999.0,"longitude":99999.0},
            {"ticket_number":1001235896,"issue_date":self.helper_to_date("2015-09-04"),"issue_time":self.helper_to_time("11:30:00"),"rp_state_plate":"CA","make":"DODG","body_style":"HS","color":"WT","agency":1,"violation_description":"NO EVIDENCE OF REG","fine_amount":50.0,"latitude":99999.0,"longitude":99999.0},
            {"ticket_number":1001235900,"issue_date":self.helper_to_date("2015-09-15"),"issue_time":self.helper_to_time("09:30:00"),"rp_state_plate":"CA","make":"MERC","body_style":"PA","color":"BK","agency":1,"violation_description":"RED ZONE","fine_amount":93.0,"latitude":99999.0,"longitude":99999.0},
            {"ticket_number":1001235911,"issue_date":self.helper_to_date("2015-09-15"),"issue_time":self.helper_to_time("09:35:00"),"rp_state_plate":"CA","make":"TOYO","body_style":"PA","color":"BK","agency":1,"violation_description":"NO EVIDENCE OF REG","fine_amount":50.0,"latitude":99999.0,"longitude":99999.0},
            {"ticket_number":1001235922,"issue_date":self.helper_to_date("2015-09-15"),"issue_time":self.helper_to_time("09:45:00"),"rp_state_plate":"CA","make":"HOND","body_style":"PA","color":"BL","agency":1,"violation_description":"NO EVIDENCE OF REG","fine_amount":50.0,"latitude":99999.0,"longitude":99999.0},
            {"ticket_number":1001235933,"issue_date":self.helper_to_date("2015-09-15"),"issue_time":self.helper_to_time("10:15:00"),"rp_state_plate":"CA","make":"TOYO","body_style":"PA","color":"GY","agency":1,"violation_description":"NO EVIDENCE OF REG","fine_amount":50.0,"latitude":99999.0,"longitude":99999.0},
            {"ticket_number":1001235955,"issue_date":self.helper_to_date("2015-12-31"),"issue_time":self.helper_to_time("19:45:00"),"rp_state_plate":"CT","make":"SUBA","body_style":"PA","color":"WT","agency":1,"violation_description":"BLOCKING DRIVEWAY","fine_amount":68.0,"latitude":99999.0,"longitude":99999.0},
            {"ticket_number":1001235966,"issue_date":self.helper_to_date("2016-02-15"),"issue_time":self.helper_to_time("01:20:00"),"rp_state_plate":"CA","make":"TOYO","body_style":"PA","color":"SI","agency":1,"violation_description":"RED ZONE","fine_amount":93.0,"latitude":99999.0,"longitude":99999.0},
            {"ticket_number":1001235970,"issue_date":self.helper_to_date("2016-02-28"),"issue_time":self.helper_to_time("10:55:00"),"rp_state_plate":"CA","make":"FORD","body_style":"TR","color":"OT","agency":1,"violation_description":"NO EVIDENCE OF REG","fine_amount":50.0,"latitude":99999.0,"longitude":99999.0}
        ]

        for item in self.data:
            Ticket.objects.create(ticket_number=item['ticket_number'], 
                                  issue_date=item['issue_date'],
                                  issue_time=item['issue_time'], 
                                  rp_state_plate=item['rp_state_plate'],
                                  make=item['make'],
                                  body_style=item['body_style'],
                                  color=item['color'], 
                                  agency=item['agency'],
                                  violation_description=item['violation_description'],
                                  fine_amount=item['fine_amount'], 
                                  latitude=item['latitude'],
                                  longitude=item['longitude'])

    def test_get_all(self):
        items = Ticket.objects.all()
        self.assertEqual(len(items), len(self.data))

    def test_filter_make(self):
        items = Ticket.objects.filter(make='TOYO')
        for ticket in items:
            self.assertEqual(ticket.make, 'TOYO')

    def test_filter_color(self):
        items = Ticket.objects.filter(color='BL')
        for ticket in items:
            self.assertEqual(ticket.color, 'BL')

    def test_filter_state(self):
        items = Ticket.objects.filter(rp_state_plate='CA')
        for ticket in items:
            self.assertEqual(ticket.rp_state_plate, 'CA')

    def test_filter_fine_upper(self):
        items = Ticket.objects.filter(fine_amount__lte=60.0)
        filtered = list(map(lambda x: x.fine_amount <= 60.0, items))
        self.assertEqual(len(filtered), len(items))

    def test_filter_fine_lower(self):
        items = Ticket.objects.filter(fine_amount__gte=60.0)
        filtered = list(map(lambda x: x.fine_amount >= 60.0, items))
        self.assertEqual(len(filtered), len(items))

    def test_filter_agency(self):
        items = Ticket.objects.filter(agency=1)
        for ticket in items:
            self.assertEqual(ticket.agency, 1)

    def test_filter_description(self):
        pass

    def test_filter_time_span(self):
        pass

    def helper_to_date(self, s):
        return s
        # return time.strptime(s, '%Y-%m-%d')

    def helper_to_time(self, t):
        return t
        # return time.strptime(t, '%H:%M:%S')

'''
https://docs.djangoproject.com/en/2.0/topics/testing/tools/#exceptions
class TicketViewTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_all(self):
        pass

    def test_filter_make(self):
        pass

    def test_filter_color(self):
        pass

    def test_filter_state(self):
        pass

    def test_filter_fine_upper(self):
        pass

    def test_filter_fine_lower(self):
        pass

    def test_filter_agency(self):
        pass

    def test_filter_description(self):
        pass

    def test_filter_time_span(self):
        pass
'''