# Generated by Django 2.0 on 2017-12-30 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketdata', '0002_auto_20171230_0655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='agency',
            field=models.SmallIntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='body_style',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='color',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fine_amount',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='latitude',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='longitude',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='make',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='rp_state_plate',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='violation_description',
            field=models.CharField(max_length=50, null=True),
        ),
    ]