# Generated by Django 4.2.3 on 2023-08-23 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_locationpublicinfo_building_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationpublicinfo',
            name='building_image',
            field=models.ImageField(blank=True, default='/static/images/no-image.jpg', max_length=200, null=True, upload_to='building_images/'),
        ),
    ]
