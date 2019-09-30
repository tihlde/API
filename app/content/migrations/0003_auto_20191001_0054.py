# Generated by Django 2.2.5 on 2019-09-30 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='allergy',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='cell',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='user',
            name='em_nr',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, 'Mann'), (2, 'Kvinne'), (3, 'Annet')], default=3, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='home_busstop',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='tool',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_class',
            field=models.IntegerField(blank=True, choices=[(1, '1. Klasse'), (2, '2. Klasse'), (3, '3. Klasse'), (4, '4. Klasse'), (5, '5. Klasse')], default=3, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_study',
            field=models.IntegerField(blank=True, choices=[(1, 'Data'), (2, 'DigFor'), (3, 'Cyber'), (4, 'Master')], default=0, null=True),
        ),
    ]
