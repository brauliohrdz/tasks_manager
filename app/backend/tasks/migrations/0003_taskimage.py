# Generated by Django 4.2.3 on 2023-10-03 22:48

import backend.tasks.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_owner_alter_task_status_alter_task_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('image', models.ImageField(upload_to=backend.tasks.models.TaskImage.image_name)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='tasks.task')),
            ],
            options={
                'verbose_name': 'TaskImage',
                'verbose_name_plural': 'TaskImages',
            },
        ),
    ]
