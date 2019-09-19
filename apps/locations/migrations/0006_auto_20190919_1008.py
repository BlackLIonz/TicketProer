# Generated by Django 2.2.4 on 2019-09-19 10:08

from django.db import migrations, models
import tools.image_funcs


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_auto_20190918_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='photo',
            field=models.ImageField(default='static/Place/none.png', upload_to=tools.image_funcs.get_image_path),
        ),
    ]
