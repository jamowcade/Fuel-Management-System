# Generated by Django 4.0.3 on 2022-12-28 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuel',
            name='delete_flag',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='fuel',
            name='status',
            field=models.CharField(choices=[('1', 'Active'), ('0', 'Inactive')], default=1, max_length=2),
        ),
    ]
