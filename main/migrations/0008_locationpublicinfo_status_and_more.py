# Generated by Django 4.2.3 on 2023-08-12 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0007_rename_organization_enginroompublicinfo_enginroom_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationpublicinfo',
            name='status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='enginroompublicinfo',
            name='usage',
            field=models.CharField(blank=True, choices=[('heating', 'گرمایشی'), ('sanitary', 'آبگرم بهداشتی'), ('both', 'هردو')], max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='locationpublicinfo',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='locationpublicinfo',
            name='meter_subscription_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='locationpublicinfo',
            name='phone_number1',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='locationpublicinfo',
            name='phone_number2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Enginroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enginroom_name', models.CharField(blank=True, max_length=200, null=True)),
                ('organization', models.CharField(blank=True, max_length=200, null=True)),
                ('administration', models.CharField(blank=True, max_length=200, null=True)),
                ('creator', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_enginrooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='enginroompublicinfo',
            name='enginroom',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.enginroom'),
        ),
        migrations.AlterField(
            model_name='locationpublicinfo',
            name='enginroom',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.enginroom'),
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
    ]