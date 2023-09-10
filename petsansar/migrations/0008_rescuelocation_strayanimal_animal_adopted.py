# Generated by Django 4.0.4 on 2023-08-02 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petsansar', '0007_donation_surrender_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='RescueLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Strayanimal',
            fields=[
                ('strayanimal_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('image', models.ImageField(upload_to='img/%y')),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='adopted',
            field=models.BooleanField(default=False),
        ),
    ]
