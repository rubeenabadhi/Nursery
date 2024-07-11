# Generated by Django 5.0 on 2024-01-12 07:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_add_plants_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('feedback', models.CharField(max_length=500)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('plant', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='review', to='home.add_plants')),
            ],
        ),
    ]