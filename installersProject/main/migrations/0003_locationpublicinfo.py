# Generated by Django 4.2.3 on 2023-07-29 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_remove_organization_installer'),
    ]

    operations = [
        migrations.CreateModel(
            name='locationPublicInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('phone_number1', models.CharField(max_length=20)),
                ('phone_number2', models.CharField(max_length=20)),
                ('building_metrage', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('meter_subscription_number', models.CharField(max_length=200)),
                ('building_image', models.ImageField(blank=True, default='building_images/default.jpg', max_length=200, null=True, upload_to='building_images/')),
                ('location', models.CharField(max_length=200)),
                ('organization', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.organization')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
