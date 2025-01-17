# Generated by Django 5.1.4 on 2025-01-08 01:16

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
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('SEED', 'Seeds'), ('FERT', 'Fertilizer'), ('PEST', 'Pesticide'), ('TOOL', 'Tools/Equipment'), ('FEED', 'Animal Feed'), ('LIVE', 'Livestock'), ('CROP', 'Crops'), ('OTHER', 'Other')], max_length=5)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(choices=[('KG', 'Kilograms'), ('G', 'Grams'), ('L', 'Liters'), ('ML', 'Milliliters'), ('UNIT', 'Units'), ('BAG', 'Bags')], max_length=4)),
                ('cost_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('supplier', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('user', 'name')},
            },
        ),
    ]
