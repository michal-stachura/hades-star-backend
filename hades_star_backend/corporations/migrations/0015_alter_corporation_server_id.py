# Generated by Django 4.1.5 on 2023-04-07 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("corporations", "0014_corporation_server_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="corporation",
            name="server_id",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
