# Generated by Django 3.2.23 on 2023-12-01 07:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cloth",
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
                ("title", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True)),
                ("price", models.PositiveIntegerField(default=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "season",
                    models.CharField(
                        choices=[
                            ("winter", "winter"),
                            ("summer", "summer"),
                            ("fall", "fall"),
                        ],
                        max_length=6,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "male"), ("female", "female")], max_length=6
                    ),
                ),
                (
                    "datetime_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("datetime_modified", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
