# Generated by Django 3.0.7 on 2020-06-28 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0004_cheatsheet"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cheatsheet",
            options={
                "verbose_name": "Cheatsheet",
                "verbose_name_plural": "Cheatsheets",
            },
        ),
        migrations.RemoveField(model_name="cheatsheet", name="desc",),
        migrations.AlterField(
            model_name="cheatsheet", name="url", field=models.URLField(max_length=600),
        ),
    ]
