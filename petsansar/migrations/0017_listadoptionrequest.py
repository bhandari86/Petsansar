# Generated by Django 4.0.4 on 2023-08-21 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('petsansar', '0016_alter_contact_phonenumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListAdoptionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('rejected', 'rejected'), ('completed', 'completed')], default='pending', max_length=20)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_requests', to='petsansar.surrender')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]