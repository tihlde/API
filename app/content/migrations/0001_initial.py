# Generated by Django 2.1.7 on 2019-05-02 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField(blank=True, max_length=600, null=True)),
                ('image_alt', models.CharField(blank=True, max_length=200, null=True)),
                ('title', models.CharField(max_length=200)),
                ('start', models.DateTimeField()),
                ('location', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(blank=True, default='')),
                ('sign_up', models.BooleanField(default=False)),
                ('priority', models.IntegerField(choices=[(0, 'Low'), (1, 'Normal'), (2, 'High')], default=0, null=True)),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField(blank=True, max_length=600, null=True)),
                ('image_alt', models.CharField(blank=True, max_length=200, null=True)),
                ('title', models.CharField(max_length=200)),
                ('ingress', models.CharField(max_length=800)),
                ('body', models.TextField(blank=True, default='')),
                ('location', models.CharField(max_length=200)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('company', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('link', models.URLField(blank=True, max_length=300, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField(blank=True, max_length=600, null=True)),
                ('image_alt', models.CharField(blank=True, max_length=200, null=True)),
                ('title', models.CharField(max_length=200)),
                ('header', models.CharField(max_length=200)),
                ('body', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Warning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=400, null=True)),
                ('type', models.IntegerField(choices=[(0, 'Error'), (1, 'Warning'), (2, 'Message')], default=0, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
