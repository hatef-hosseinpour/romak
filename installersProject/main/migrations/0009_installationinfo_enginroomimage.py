# Generated by Django 4.2.3 on 2023-08-12 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_locationpublicinfo_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstallationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installed_device_model', models.CharField(blank=True, choices=[('8relays', '8relays'), ('12relays', '12relays'), ('16relays', '16relays')], max_length=2000, null=True)),
                ('connection_type', models.CharField(blank=True, choices=[('internet', 'internet'), ('intranet', 'interanet'), ('ethernet', 'ethernet ')], max_length=2000, null=True)),
                ('modem_model', models.CharField(blank=True, max_length=200, null=True)),
                ('has_simcard', models.BooleanField(default=False, null=True)),
                ('modem_simcard_number', models.CharField(blank=True, max_length=200, null=True)),
                ('installation_date', models.DateTimeField(blank=True, null=True, verbose_name='installed_at')),
                ('device_serial_number_image', models.ImageField(blank=True, default='device_serial_number/no-image.jpg', null=True, upload_to='device_serial_number/')),
                ('status', models.BooleanField(default=False, null=True)),
                ('enginroom', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.enginroom')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EnginRoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, max_length=200, null=True, upload_to='')),
                ('status', models.BooleanField(default=False, null=True)),
                ('enginroom', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.enginroom')),
                ('installation', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.installationinfo')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]