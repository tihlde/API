# Generated by Django 3.1.5 on 2021-01-19 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0015_auto_20201210_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikipost',
            name='description',
        ),
    ]