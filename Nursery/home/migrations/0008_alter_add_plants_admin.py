# Generated by Django 5.0 on 2024-01-14 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_plant_admin_password1'),
        ('home', '0007_alter_add_plants_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_plants',
            name='admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='plants', to='account.plant_admin'),
        ),
    ]
