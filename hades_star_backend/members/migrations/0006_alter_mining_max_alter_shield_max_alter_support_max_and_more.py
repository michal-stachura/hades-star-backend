# Generated by Django 4.1.5 on 2023-01-27 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "members",
            "0005_remove_support_members_support_max_value__gt_1_or_lt_12_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="mining",
            name="max",
            field=models.PositiveSmallIntegerField(default=12),
        ),
        migrations.AlterField(
            model_name="shield",
            name="max",
            field=models.PositiveSmallIntegerField(default=12),
        ),
        migrations.AlterField(
            model_name="support",
            name="max",
            field=models.PositiveSmallIntegerField(default=12),
        ),
        migrations.AlterField(
            model_name="trade",
            name="max",
            field=models.PositiveSmallIntegerField(default=12),
        ),
        migrations.AlterField(
            model_name="weapon",
            name="max",
            field=models.PositiveSmallIntegerField(default=12),
        ),
    ]
