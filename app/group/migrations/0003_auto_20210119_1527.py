# Generated by Django 3.1.5 on 2021-01-19 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_membership_membershiphistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershiphistory',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='membershiphistory',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
