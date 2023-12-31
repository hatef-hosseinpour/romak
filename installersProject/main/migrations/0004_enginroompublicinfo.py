# Generated by Django 4.2.3 on 2023-07-29 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_locationpublicinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnginRoomPublicInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage', models.CharField(choices=[('heating', 'گرمایشی'), ('sanitary', 'آبگرم بهداشتی'), ('both_heating_sanitary', 'هردو')], max_length=2000)),
                ('has_exchanger', models.BooleanField(default=False)),
                ('number_of_pool_exchangers', models.PositiveIntegerField(default=0)),
                ('number_of_jaccuzi_exchangers', models.PositiveIntegerField(default=0)),
                ('number_of_floor_heating_exchangers', models.PositiveIntegerField(default=0)),
                ('number_of_boilers', models.PositiveIntegerField(default=0)),
                ('number_of_circulating_pumps', models.PositiveIntegerField(default=0)),
                ('number_of_coil_sources', models.PositiveIntegerField(default=0)),
                ('number_of_coil_sources_pumps', models.PositiveIntegerField(default=0)),
                ('number_of_hot_water_pumps', models.PositiveIntegerField(default=0)),
                ('organization', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.organization')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
