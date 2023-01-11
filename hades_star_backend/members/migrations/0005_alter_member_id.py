# Generated by Django 4.0.8 on 2023-01-11 15:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_alter_member_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='id',
            field=models.UUIDField(default=uuid.UUID('60358dae-0370-4292-9070-3d6a3d52e35c'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
