# Generated by Django 4.0.4 on 2023-08-02 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petsansar', '0008_rescuelocation_strayanimal_animal_adopted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Strayanimalrescue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.IntegerField(max_length=10)),
                ('location', models.CharField(max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='img/%y')),
                ('date_reported', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
    ]
