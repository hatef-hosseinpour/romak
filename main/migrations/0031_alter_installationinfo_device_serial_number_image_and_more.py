# Generated by Django 4.2.3 on 2023-11-14 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_enginroom_rejection_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installationinfo',
            name='device_serial_number_image',
            field=models.ImageField(blank=True, default='device_serial_number_images/no-image.jpg', null=True, upload_to='device_serial_number_images/'),
        ),
        migrations.AlterField(
            model_name='installationinfo',
            name='modem_simcard_serial_number_image',
            field=models.ImageField(blank=True, default='modem_simcard_serial_number_images/no-image.jpg', null=True, upload_to='modem_simcard_serial_number_images/'),
        ),
        migrations.AlterField(
            model_name='locationpublicinfo',
            name='building_image',
            field=models.ImageField(blank=True, default='building_images/no-image.jpg', max_length=200, null=True, upload_to='building_images/'),
        ),
    ]
