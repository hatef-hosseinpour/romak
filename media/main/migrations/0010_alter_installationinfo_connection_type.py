# Generated by Django 4.2.3 on 2023-08-15 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_installationinfo_enginroomimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installationinfo',
            name='connection_type',
            field=models.CharField(blank=True, choices=[('internet', 'internet'), ('intranet', 'intranet'), ('ethernet', 'ethernet')], max_length=2000, null=True),
        ),
    ]
