# Generated by Django 2.2.4 on 2019-08-26 13:48

from django.db import migrations, models
import tools.image_funcs


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=tools.image_funcs.get_place_photo_path),
        ),
        migrations.AlterField(
            model_name='place',
            name='status',
            field=models.CharField(choices=[('TEMPORARILY_CLOSED', 'Temporarily closed'), ('WORKING', 'Working'), ('CLOSED', 'Closed')], max_length=18),
        ),
    ]