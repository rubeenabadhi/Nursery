# Generated by Django 5.0 on 2024-02-15 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_alter_ordermanagement_order_date'),
        ('home', '0010_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermanagement',
            name='plant',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='home.add_plants'),
        ),
    ]
