# Generated by Django 4.0.4 on 2023-08-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petsansar', '0013_remove_adoptionrequest_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='adoptionrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('rejected', 'rejected'), ('completed', 'completed')], default='pending', max_length=20),
        ),
    ]
