# Generated by Django 2.0.7 on 2018-08-04 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('start', models.DateTimeField()),
                ('location', models.CharField(max_length=200, null=True)),
                ('description', models.TextField()),
                ('sign_up', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField(max_length=400, null=True)),
                ('image_alt', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('order', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ManualGridItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('priority', models.IntegerField()),
            ],
            options={
                'ordering': ['-priority'],
            },
        ),
        migrations.CreateModel(
            name='EventList',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.Item')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.item',),
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.Item')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.item',),
        ),
        migrations.CreateModel(
            name='ManualGrid',
            fields=[
                ('grid_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.Grid')),
            ],
            options={
                'abstract': False,
            },
            bases=('content.grid',),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.Item')),
                ('image', models.URLField(max_length=400, null=True)),
                ('image_alt', models.CharField(max_length=200, null=True)),
                ('title', models.CharField(max_length=200)),
                ('header', models.CharField(max_length=200)),
                ('body', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('content.item', models.Model),
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.Item')),
                ('image', models.URLField(max_length=400, null=True)),
                ('image_alt', models.CharField(max_length=200, null=True)),
                ('action', models.URLField(blank=True, null=True)),
                ('action_text', models.CharField(blank=True, max_length=200, null=True)),
                ('header', models.CharField(blank=True, max_length=200)),
                ('subheader', models.CharField(blank=True, max_length=200)),
                ('color', models.CharField(blank=True, max_length=7)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.item', models.Model),
        ),
        migrations.CreateModel(
            name='RecentFirstGrid',
            fields=[
                ('grid_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.Grid')),
                ('item_class', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=('content.grid',),
        ),
        migrations.AddField(
            model_name='manualgriditem',
            name='item',
            field=models.ForeignKey(on_delete='CASCADE', to='content.Item'),
        ),
        migrations.AddField(
            model_name='manualgriditem',
            name='grid',
            field=models.ForeignKey(on_delete='CASCADE', to='content.ManualGrid'),
        ),
        migrations.AddField(
            model_name='manualgrid',
            name='items',
            field=models.ManyToManyField(through='content.ManualGridItem', to='content.Item'),
        ),
        migrations.AddField(
            model_name='image',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='content.ImageGallery'),
        ),
        migrations.AddField(
            model_name='event',
            name='eventlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='content.EventList'),
        ),
    ]
