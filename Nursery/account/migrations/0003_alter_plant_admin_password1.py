# Generated by Django 5.0 on 2024-01-14 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_plant_admin_password2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant_admin',
            name='password1',
            field=models.CharField(max_length=20),
        ),
    ]