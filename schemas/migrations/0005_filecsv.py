# Generated by Django 4.1.4 on 2022-12-14 00:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("schemas", "0004_alter_schema_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="FileCSV",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file_name", models.CharField(max_length=255, unique=True)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "rows",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "schema",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="schemas.schema",
                    ),
                ),
            ],
        ),
    ]