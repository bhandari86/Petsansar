# Generated by Django 4.0.4 on 2023-08-04 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petsansar', '0012_remove_adoptionrequest_medical_condition_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adoptionrequest',
            name='location',
        ),
    ]
