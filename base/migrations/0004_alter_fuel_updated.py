# Generated by Django 4.0.3 on 2022-12-29 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_fuel_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuel',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]