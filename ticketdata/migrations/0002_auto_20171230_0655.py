# Generated by Django 2.0 on 2017-12-30 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketdata', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='issute_time',
            new_name='issue_time',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_number',
            field=models.IntegerField(),
        ),
    ]