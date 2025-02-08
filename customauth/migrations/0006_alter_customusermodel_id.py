# Generated by Django 5.2a1 on 2025-02-06 10:12

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customauth', '0005_alter_customusermodel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
