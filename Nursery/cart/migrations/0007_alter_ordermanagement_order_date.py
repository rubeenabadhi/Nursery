# Generated by Django 5.0 on 2024-02-15 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_ordermanagement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermanagement',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
