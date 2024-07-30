# Generated by Django 5.0.6 on 2024-07-03 23:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('turnero', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turnero.usuarios')),
            ],
        ),
    ]