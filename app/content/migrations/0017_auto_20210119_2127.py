# Generated by Django 3.1.5 on 2021-01-19 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_remove_wikipost_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikipost',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
