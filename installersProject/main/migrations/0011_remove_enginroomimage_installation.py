# Generated by Django 4.2.3 on 2023-08-16 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_installationinfo_connection_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enginroomimage',
            name='installation',
        ),
    ]
