# Generated by Django 4.2.3 on 2023-08-22 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_enginroomimage_installation'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationpublicinfo',
            name='step',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
