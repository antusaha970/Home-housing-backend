# Generated by Django 5.0.6 on 2024-07-06 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0003_alter_advertisement_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisementimages',
            name='image',
            field=models.ImageField(upload_to='rent/advertisement/'),
        ),
    ]