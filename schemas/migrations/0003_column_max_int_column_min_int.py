# Generated by Django 4.1.4 on 2022-12-11 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schemas", "0002_alter_schema_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="column",
            name="max_int",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="column",
            name="min_int",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
