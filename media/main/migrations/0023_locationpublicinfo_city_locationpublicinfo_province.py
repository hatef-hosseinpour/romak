# Generated by Django 4.2.3 on 2023-09-16 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_alter_enginroomimage_enginroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationpublicinfo',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='locationpublicinfo',
            name='province',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]