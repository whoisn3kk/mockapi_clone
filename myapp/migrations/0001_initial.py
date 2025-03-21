# Generated by Django 5.0.7 on 2024-08-03 11:21

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255, unique=True)),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.JSONField(default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.users')),
            ],
        ),
    ]
