# Generated by Django 4.0.4 on 2023-08-25 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petsansar', '0019_surrender_medical_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strayanimalrescue',
            name='phone',
            field=models.TextField(blank=True, max_length=10, null=True),
        ),
    ]
