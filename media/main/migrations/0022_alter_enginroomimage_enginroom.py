# Generated by Django 4.2.3 on 2023-08-29 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_installationinfo_device_serial_number_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enginroomimage',
            name='enginroom',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.enginroom'),
        ),
    ]
