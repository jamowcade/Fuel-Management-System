# Generated by Django 4.0.3 on 2022-12-26 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('price', models.FloatField(default=0, max_length=(15, 2))),
                ('user', models.CharField(blank=True, max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'fuel type lists',
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.FloatField(default=0, max_length=(15, 2))),
                ('user', models.CharField(blank=True, max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('fuel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.fuel')),
            ],
            options={
                'verbose_name_plural': 'Stock lists',
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=200)),
                ('volume', models.FloatField(default=0, max_length=(15, 2))),
                ('amount', models.FloatField(default=0, max_length=(15, 2))),
                ('user', models.CharField(blank=True, max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('fuel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.fuel')),
            ],
            options={
                'verbose_name_plural': 'Sales list',
                'ordering': ['-updated', '-created'],
            },
        ),
    ]
