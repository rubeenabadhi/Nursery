# Generated by Django 5.0 on 2024-01-12 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_add_plants_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_plants',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]