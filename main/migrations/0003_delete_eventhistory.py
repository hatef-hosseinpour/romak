# Generated by Django 4.2.3 on 2024-02-18 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_eventhistory_device_remove_eventhistory_text_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventHistory',
        ),
    ]