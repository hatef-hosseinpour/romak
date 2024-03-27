# Generated by Django 4.2.3 on 2024-02-25 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='device name')),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('key', models.CharField(blank=True, max_length=100, unique=True)),
                ('installation_address', models.CharField(default='', max_length=500)),
                ('active', models.BooleanField(default=True)),
                ('step', models.IntegerField(blank=True, default=0, null=True)),
                ('status', models.BooleanField(blank=True, default=None, null=True)),
                ('rejection_note', models.TextField(blank=True, default='', null=True)),
                ('created_by', models.IntegerField(blank=True, default=1, null=True)),
                ('details', models.JSONField(null=True)),
                ('lat_long', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
            options={
                'db_table': 'main_device',
                'ordering': ['-id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EngineRoomFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_3d_view', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'main_engineroomfeature',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='', max_length=100)),
                ('province', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'main_location',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(default='', max_length=100)),
                ('administration', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'main_organization',
                'managed': False,
            },
        ),
    ]