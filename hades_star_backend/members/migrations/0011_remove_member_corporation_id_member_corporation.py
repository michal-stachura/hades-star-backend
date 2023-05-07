# Generated by Django 4.1.5 on 2023-04-15 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "corporations",
            "0017_remove_corporation_corporation_server_id__gte_0_and_more",
        ),
        ("members", "0010_remove_member_corporation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="corporation_id",
        ),
        migrations.AddField(
            model_name="member",
            name="corporation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="member_corporation",
                to="corporations.corporation",
            ),
        ),
    ]
