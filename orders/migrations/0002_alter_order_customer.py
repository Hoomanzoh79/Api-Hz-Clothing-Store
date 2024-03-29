# Generated by Django 3.2.24 on 2024-02-17 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='accounts.profile'),
        ),
    ]
