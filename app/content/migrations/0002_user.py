# Generated by Django 2.1.7 on 2019-09-30 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField(blank=True, max_length=600, null=True)),
                ('image_alt', models.CharField(blank=True, max_length=200, null=True)),
                ('user_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('cell', models.CharField(max_length=8)),
                ('em_nr', models.CharField(max_length=12)),
                ('home_busstop', models.IntegerField()),
                ('gender', models.IntegerField(choices=[(1, 'Mann'), (2, 'Kvinne'), (3, 'Annet')], default=0, null=True)),
                ('user_class', models.IntegerField(choices=[(1, 'Første'), (2, 'Andre'), (3, 'Tredje'), (4, 'Fjerde'), (5, 'Femte')], default=0, null=True)),
                ('user_study', models.IntegerField(choices=[(1, 'Data'), (2, 'DigFor'), (3, 'Cyber'), (4, 'Master')], default=0, null=True)),
                ('allergy', models.TextField()),
                ('tool', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
