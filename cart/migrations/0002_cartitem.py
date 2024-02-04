# Generated by Django 3.2.23 on 2024-02-03 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloths', '0006_alter_comment_author'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='cart.cart')),
                ('cloth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cloths.cloth')),
            ],
            options={
                'unique_together': {('cart', 'cloth')},
            },
        ),
    ]