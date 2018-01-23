from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.db.models import Avg, Max, Min, Count

from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import generics
from rest_framework import exceptions

from ticket_data_vis.pagination import TicketsOffsetPagination

from . import DateCount, DayStats, MonthStats
from ticketdata.models import Ticket
from ticketdata.serializers import TicketSerializer, DateCountSerializer, DayStatsSerializer, MonthStatsSerializer

# Create your views here.
def index(request):
    return HttpResponse("Hello gus I am working")

class TicketViewSet(generics.ListAPIView):
    serializer_class = TicketSerializer
    pagination = TicketsOffsetPagination
    def get_queryset(self):
        return create_tickets_filter_query_set(self.request)

class AverageFineAmountView(APIView):
    def get(self, request, format=None):
        qs = create_tickets_filter_query_set(request)
        _a = qs.aggregate(Avg('fine_amount'), Max('fine_amount'), Min('fine_amount'))
        # Add StdDev, but be aware that it will not work on sqlit3

        return Response(
            {
                'avg':_a['fine_amount__avg'],
                'max':_a['fine_amount__max'],
                'min':_a['fine_amount__min']
            })

class CarColorCountsView(APIView):
    def get(self, request, format=None):
        qs = create_tickets_filter_query_set(request)
        counts = qs.values('color').annotate(count=Count('color')).order_by('color')
        for item in counts:
            color_code = item['color']
            if color_code in color_dict:
                item['color'] = color_dict[color_code]
        return Response(counts)  

class StatePlatesCountView(APIView):
    def get(self, request, format=None):
        qs = create_tickets_filter_query_set(request)
        counts = qs.values('rp_state_plate').annotate(count=Count('rp_state_plate')).order_by('rp_state_plate')
        for item in counts:
            state_code = item['rp_state_plate']
            if state_code in state_dict:
                item['rp_state_plate'] = state_dict[state_code]
        return Response(counts)

class AgenciesCountView(APIView):
    def get(self, request, format=None):
        qs = create_tickets_filter_query_set(request)
        counts = qs.values('agency').annotate(count=Count('agency')).order_by('agency')
        for item in counts:
            agency_code = str(item['agency'])
            if agency_code in agencies_dict:
                item['agency'] = agencies_dict[agency_code]
            else: 
                item['agency'] = agency_code             
        return Response(counts)

class CountByDay(APIView):
    def get(self, request, format=None):
        values = []
        with connection.cursor() as cursor:
            select_statement = "SELECT issue_date as date, COUNT(*) as 'count' FROM ticketdata_ticket "
            group_by_clause =  " GROUP BY issue_date "
            sql_statement, sql_params = createSQLStatement(select_statement, group_by_clause, request)
            cursor.execute(sql_statement, sql_params)
            values = map(lambda x: DateCount(date=x[0], count=x[1]), cursor.fetchall())
        serializer = DateCountSerializer(instance=values, many=True)
        return Response(serializer.data)

class FineAvgStdyDayofWeek(APIView):
    def get(self, request, format=None):
        values = []
        with connection.cursor() as cursor:
            if settings.DEBUG:
                select_statement = "SELECT strftime('%%w', `issue_date`), AVG(`fine_amount`) FROM `ticketdata_ticket` "
                group_by_clause =  " GROUP BY strftime('%%w', `issue_date`) "
                sql_statement, sql_params = createSQLStatement(select_statement, group_by_clause, request)
                cursor.execute(sql_statement, sql_params)
                values = map(lambda x: DayStats(day=x[0], avg=x[1]), cursor.fetchall())
            else:
                select_statement = "SELECT WEEKDAY(`issue_date`), AVG(`fine_amount`),STDDEV(`fine_amount`) FROM `ticketdata_ticket` "
                group_by_clause =  " GROUP BY WEEKDAY(`issue_date`) "
                sql_statement, sql_params = createSQLStatement(select_statement, group_by_clause, request)
                cursor.execute(sql_statement, sql_params)
                values = map(lambda x: DayStats(day=x[0], avg=x[1], std=x[2]), cursor.fetchall())                
        serializer = DayStatsSerializer(instance=values, many=True)
        return Response(serializer.data)

class FineAvgStdyMonthofYear(APIView):
    def get(self, request, format=None):
        values = []
        with connection.cursor() as cursor:
            if settings.DEBUG:
                select_statement = "SELECT strftime('%%m', `issue_date`), AVG(`fine_amount`) FROM `ticketdata_ticket` "
                group_by_clause =  " GROUP BY strftime('%%m', `issue_date`) "
                sql_statement, sql_params = createSQLStatement(select_statement, group_by_clause, request)
                cursor.execute(sql_statement, sql_params)
                values = map(lambda x: MonthStats(month=x[0], avg=x[1]), cursor.fetchall())
            else:
                select_statement = "SELECT MONTH(`issue_date`), AVG(`fine_amount`), STDDEV(`fine_amount`) FROM `ticketdata_ticket` "
                group_by_clause = " GROUP BY MONTH(`issue_date`) "
                sql_statement, sql_params = createSQLStatement(select_statement, group_by_clause, request)
                cursor.execute(sql_statement, sql_params)
                values = map(lambda x: MonthStats(month=x[0], avg=x[1], std=x[2]), cursor.fetchall())
        serializer = MonthStatsSerializer(instance=values, many=True)
        return Response(serializer.data)

''' -- -- -- -- HELPER FUNCTIONS START -- -- -- -- '''

color_dict = {"BG":"Beige", "BK":"Black", "BL":"Blue", "BN":"Brown", "GD":"Gold", "GN":"Green", "GY":"Gray", "MR":"Maroon", "OR":"Orange", "OT":"Other", "PK":"Pink", "RD":"Red", "SI":"Silver", "TN":"Tan", "WT":"White", "YL":"Yellow", "VT":"Violet"}
state_dict = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming', 'GU': 'Guam', 'PR': 'Puerto Rico', 'VI': 'Virgin Islands', 'MX':'Mexico', 'CN':'Canada', 'DC':'Washington DC', 'XX':'Unknown'}
agencies_dict = {'1': 'WESTERN', '2': 'LAX CURRENT', '3': 'VALLEY', '4': 'HOLLYWOOD', '5': 'SOUTHERN', '6': 'CENTRAL', '7': 'HPV', '8': 'AIRPORT BACK', '9': 'BANDIT CAB TASK FORCE', '10': 'LAPD BACKLOG', '11': 'VN AIRPORT', '12': 'PARK RANGERS', '14': 'MARSHALLS OFFICE', '15': 'PUBLIC UTILITIES', '16': 'ANIMAL REGULATION DEPARTMENT', '17': 'LASD - CITY ENFORCEMENT', '18': 'CONVENTION CENTER', '20': 'CALIFORNIA HIGHWAY PATROL', '21': 'CALIFORNIA STATE POLICE', '22': 'CA PARKS & REC', '34': 'GENERAL SERVICES DEPARTMENT', '35': 'AMTRAK POLICE DEPT', '40': 'BUILDING AND SAFETY', '41': 'STREET USE INSPECTORS', '44': 'LIBRARY - SECURITY FORCE', '50': 'DOT - HARBOR', '51': 'DOT - WESTERN', '52': 'DOT - WILSHIRE', '53': 'DOT - VALLEY', '54': 'DOT - HOLLYWOOD', '55': 'DOT - SOUTHERN', '56': 'DOT - CENTRAL', '57': 'HABITUAL VIOLATORS', '58': 'SPECIAL EVENTS', '59': 'DOT-DISABLED PLACARD TASK FORCE', '60': 'DOT - RESIDENTIAL TASK FORCE', '61': 'CORT METRO', '62': 'CORT VALLEY', '63': 'EMERGENCY DETAIL', '64': 'SPECIAL ENFORCEMEN-DOT HOLLYWOOD', '65': 'SPECIAL ENFORCEMENT-DOT SOUTHERN', '66': 'SPECIAL ENFORCEMENT-DOT CENTRAL', '71': 'METRO ABATEMENT', '72': 'VALLEY ABATEMENT', '75': 'US FEDERAL PROTECTIVE SERV', '80': 'D.O.T WESTERN', '81': 'D.O.T. WILSHIRE', '82': 'D.O.T. VALLEY', '83': 'D.O.T. HOLLYWOOD', '84': 'D.O.T. SOUTHERN', '85': 'D.O.T. CENTRAL', '86': 'HABITUAL VIOLS', '87': 'SPECIAL EVENTS', '88': 'LAPD CURRENT', '89': 'LAPD BACKLOG', '90': 'AIRPORT CURRENT', '91': 'AIRPORT BACKLOG', '92': 'HARBOR', '93': 'PARKS AND REC', '94': 'FIRE DEPARTMENT', '95': 'HOUSING AUTHORITY', '96': 'RANGERS', '97': 'HOUSING DEPARTMENT'}

def create_tickets_filter_query_set(request):
    qs = Ticket.objects.all()

    if 'color' in request.query_params:
        p_color = str(request.query_params['color']).upper()
        qs = qs.filter(color=p_color)

    if 'state' in request.query_params:
        p_state = str(request.query_params['state']).upper()
        qs = qs.filter(rp_state_plate=p_state)

    if 'fine_upper'in request.query_params:
        try:
            p_fine_upper = float(str(request.query_params['fine_upper']))
            qs = qs.filter(fine_amount__lte=p_fine_upper)
        except:
            raise exceptions.NotFound(detail="Make sure fine_upper is a number")
    
    if 'fine_lower'in request.query_params:
        try:
            p_fine_lower = float(str(request.query_params['fine_lower']))
            qs = qs.filter(fine_amount__gte=p_fine_lower)
        except:
            raise exceptions.NotFound(detail="Make sure fine_lower is a number")
    
    if 'agency'in request.query_params:
        p_agency = str(request.query_params['agency']).upper()
        qs = qs.filter(agency=p_agency)

    if 'violation_description'in request.query_params:
        p_description = str(request.query_params['violation_description']).upper()[:25]
        qs = qs.filter(violation_description__contains=p_description)

    if 'make'in request.query_params:
        p_make = str(request.query_params['make']).upper()[:4]
        qs = qs.filter(make=p_make)

    if 'start_date'in request.query_params and 'end_date'in request.query_params:
        try:
            start_date = datetime.strptime(request.query_params['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.query_params['end_date'], '%Y-%m-%d')
            qs = qs.filter(issue_date__range=(start_date, end_date))
        except:
            raise exceptions.NotFound(detail="Check the format of start_date and end_date.")
    
    return qs

def createSQLStatement(select_statement, group_by_clause, request):
    where_clause_tuple = create_where_clause(request)
    where_clause = where_clause_tuple[0]
    sql_params = where_clause_tuple[1]
    return (select_statement + where_clause + group_by_clause, sql_params)

def create_where_clause(request):
    where_params = []
    where_clause = ''

    if 'color' in request.query_params:
        where_clause = where_clause + "AND color = %s "
        where_params.append(str(request.query_params['color']).upper())

    if 'state' in request.query_params:
        where_clause = where_clause + 'AND rp_state_plate = %s '
        where_params.append(str(request.query_params['state']).upper())

    if 'fine_upper'in request.query_params:
        try:
            where_clause = where_clause + 'AND fine_amount <= %s '
            where_params.append(float(str(request.query_params['fine_upper'])))
        except:
            raise exceptions.NotFound(detail="Make sure fine_upper is a number")
    
    if 'fine_lower'in request.query_params:
        try:
            where_clause = where_clause + 'AND fine_amount >= %s '
            where_params.append(float(str(request.query_params['fine_lower'])))
        except:
            raise exceptions.NotFound(detail="Make sure fine_lower is a number")
    
    if 'agency'in request.query_params:
        where_clause = where_clause + 'AND agency = %s '
        where_params.append(str(request.query_params['agency']).upper())

    if 'violation_description'in request.query_params:
        where_clause = where_clause + 'AND violation_description LIKE %s'
        where_params.append(str(request.query_params['violation_description']).upper()[:25])

    if 'make'in request.query_params:
        where_clause = where_clause + 'AND make = %s'
        where_params.append(str(request.query_params['make']).upper()[:4])

    '''if 'start_date'in request.query_params and 'end_date'in request.query_params:
        try:
            where_clause = where_clause + 'AND rp_state_plate=%s'
            where_params.append(str(request.query_params['state']).upper())

            start_date = datetime.strptime(request.query_params['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.query_params['end_date'], '%Y-%m-%d')
            qs = qs.filter(issue_date__range=(start_date, end_date))
        except:
            raise exceptions.NotFound(detail="Check the format of start_date and end_date.")'''
    
    if len(where_clause) > 0:
        where_clause = "WHERE" + where_clause[3:]

    return (where_clause, where_params)

''' -- -- -- -- HELPER FUNCTIONS END -- -- -- -- '''
