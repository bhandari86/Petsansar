# Generated by Django 4.0.4 on 2023-07-28 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petsansar', '0002_animal'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='animaltype',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='animal',
            name='desc',
            field=models.TextField(default='', max_length=100),
        ),
    ]