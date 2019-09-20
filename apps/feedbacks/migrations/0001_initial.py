# Generated by Django 2.2.4 on 2019-09-20 14:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('text', models.TextField()),
                ('parent_object_id', models.UUIDField(editable=False)),
                ('status', models.CharField(choices=[('OK', 'ok'), ('SUSPICIOUS', 'suspicious'), ('DELETED', 'deleted')], default='OK', max_length=16)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('parent_object_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'unique_together': {('parent_object_id', 'created_by')},
            },
        ),
    ]
