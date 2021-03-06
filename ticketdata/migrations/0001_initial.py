# Generated by Django 2.0 on 2017-12-29 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number', models.FloatField(unique=True)),
                ('issue_date', models.DateField()),
                ('issute_time', models.TimeField()),
                ('rp_state_plate', models.CharField(max_length=2)),
                ('make', models.CharField(max_length=4)),
                ('body_style', models.CharField(max_length=2)),
                ('color', models.CharField(max_length=2)),
                ('agency', models.SmallIntegerField(default=-1)),
                ('violation_description', models.CharField(max_length=50)),
                ('fine_amount', models.FloatField(default=0.0)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
            ],
        ),
    ]
