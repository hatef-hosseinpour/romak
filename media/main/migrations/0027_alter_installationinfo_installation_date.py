# Generated by Django 4.2.3 on 2023-09-25 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_enginroom_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installationinfo',
            name='installation_date',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='installed_at'),
        ),
    ]
