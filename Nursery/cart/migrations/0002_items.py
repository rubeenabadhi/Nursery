# Generated by Django 5.0 on 2024-01-01 11:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('home', '0002_alter_add_plants_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cartlist')),
                ('plant_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.add_plants')),
            ],
        ),
    ]
