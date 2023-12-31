# Generated by Django 4.2.3 on 2023-10-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_added_by_profile_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='default_user.jpg', max_length=200, null=True, upload_to='uploads/profile_images/'),
        ),
    ]
