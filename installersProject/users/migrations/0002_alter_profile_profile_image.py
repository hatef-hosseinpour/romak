# Generated by Django 4.2.3 on 2023-08-27 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='default_user.jpg', max_length=200, null=True, upload_to='profile_images/'),
        ),
    ]
