# Generated by Django 4.2.3 on 2024-02-03 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teska_main', '0005_engineroomfeature'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={'managed': False, 'ordering': ['-id']},
        ),
    ]
