# Generated by Django 2.2.4 on 2019-09-02 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20190830_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='place', to='locations.Address'),
        ),
    ]
