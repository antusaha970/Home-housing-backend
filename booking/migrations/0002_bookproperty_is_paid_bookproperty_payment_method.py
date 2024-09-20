# Generated by Django 5.0.6 on 2024-07-14 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookproperty',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bookproperty',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'cash'), ('card', 'card')], default='cash', max_length=10),
        ),
    ]