# Generated by Django 4.2.3 on 2024-02-24 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_locationpublicinfo_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationpublicinfo',
            name='linker_person1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='locationpublicinfo',
            name='linker_person2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]