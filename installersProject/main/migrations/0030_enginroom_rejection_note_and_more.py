# Generated by Django 4.2.3 on 2023-10-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_rename_images_enginroomimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='enginroom',
            name='rejection_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='installationinfo',
            name='modem_simcard_serial_number_image',
            field=models.ImageField(blank=True, default='no-image.jpg', null=True, upload_to='modem_simcard_serial_number_images/'),
        ),
    ]
