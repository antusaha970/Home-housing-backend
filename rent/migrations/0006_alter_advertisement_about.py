# Generated by Django 5.0.6 on 2024-07-10 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0005_userfavoriteadvertisement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='about',
            field=models.TextField(),
        ),
    ]
