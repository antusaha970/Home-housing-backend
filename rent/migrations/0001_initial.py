# Generated by Django 5.0.6 on 2024-07-06 08:09

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('body', models.TextField()),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin_approved', models.BooleanField(default=False)),
                ('is_booked', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('home', 'home'), ('family', 'family'), ('office', 'office'), ('bachelor', 'bachelor'), ('shop', 'shop'), ('sublet', 'sublet'), ('hostel', 'hostel')], default='family', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('division', models.CharField(default='', max_length=255)),
                ('district', models.CharField(default='', max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('bedrooms', models.IntegerField(default=0)),
                ('bathrooms', models.IntegerField(default=0)),
                ('about', models.CharField(default='', max_length=300)),
                ('summary', models.TextField(default='')),
                ('title', models.CharField(max_length=255)),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdvertisementImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='rest/advertisement/')),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisement_image', to='rent.advertisement')),
            ],
        ),
        migrations.CreateModel(
            name='AdvertisementReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisement_review', to='rent.advertisement')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent.review')),
            ],
        ),
    ]