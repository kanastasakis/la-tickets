from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url('data/', views.TicketViewSet.as_view()),
    url('average/', views.AverageFineAmountView.as_view()),
    url('color/', views.CarColorCountsView.as_view()),
    url('state/', views.StatePlatesCountView.as_view()),
    url('agency/', views.AgenciesCountView.as_view()),
    url('day/', views.CountByDay.as_view()),
    url('avgdayofweek/', views.FineAvgStdyDayofWeek.as_view()),
    url('avgmonthofyear/', views.FineAvgStdyMonthofYear.as_view()),
]