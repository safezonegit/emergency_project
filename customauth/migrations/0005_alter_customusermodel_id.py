# Generated by Django 5.1.5 on 2025-01-20 15:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customauth', '0004_alter_customusermodel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='id',
            field=models.UUIDField(default=uuid.UUID('77dfbdfa-0a2e-491f-b477-a7d30d430a07'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
