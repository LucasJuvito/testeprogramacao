# Generated by Django 4.0.2 on 2022-02-11 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=255)),
                ('produto', models.CharField(max_length=255)),
                ('valor', models.FloatField()),
                ('entregue', models.BooleanField()),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
