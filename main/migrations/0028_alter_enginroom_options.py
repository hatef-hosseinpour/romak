# Generated by Django 4.2.3 on 2023-09-26 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_alter_installationinfo_installation_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enginroom',
            options={'ordering': ['-id']},
        ),
    ]
