# Generated by Django 4.0.8 on 2023-01-11 15:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('corporations', '0004_alter_corporation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporation',
            name='id',
            field=models.UUIDField(default=uuid.UUID('261d4e5c-4505-4d3f-a1ea-90bd7b9ccd04'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
