# Generated by Django 2.2.4 on 2019-09-25 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('OK', 'ok'), ('SUSPICIOUS', 'suspicious'), ('DELETED', 'deleted')], default='OK', max_length=16),
        ),
    ]
