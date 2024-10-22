# Generated by Django 5.0 on 2023-12-29 12:40

import autoslug.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='categ_plants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='add_plants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='name')),
                ('img', models.ImageField(upload_to='pictures')),
                ('price', models.IntegerField()),
                ('details', models.TextField()),
                ('available', models.BooleanField(default=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.categ_plants')),
            ],
        ),
    ]
