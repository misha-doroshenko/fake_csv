# Generated by Django 4.1.4 on 2022-12-14 06:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("schemas", "0005_filecsv"),
    ]

    operations = [
        migrations.AddField(
            model_name="filecsv",
            name="file_path",
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
