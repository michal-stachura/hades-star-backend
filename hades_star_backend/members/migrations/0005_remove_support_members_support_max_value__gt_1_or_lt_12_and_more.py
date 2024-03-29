# Generated by Django 4.1.5 on 2023-01-22 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0004_alter_weapon_name"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="support",
            name="members_support_max_value__gt_1_or_lt_12",
        ),
        migrations.AlterField(
            model_name="support",
            name="name",
            field=models.CharField(
                choices=[
                    ("EMP", "Emp"),
                    ("TELEPORT", "Teleport"),
                    ("RED_STAR_LIFE_EXTENDER", "Red Star life extender"),
                    ("REMOTE_REPAIR", "Remote repair"),
                    ("TIME_WRAP", "Time Warp"),
                    ("UNITY", "Unity"),
                    ("SANCTUARY", "Sanctuary"),
                    ("STEALTH", "Stealth"),
                    ("FORTIFY", "Fortify"),
                    ("IMPULSE", "Impulse"),
                    ("ALPHA_ROCKET", "Alpha rocket"),
                    ("SALVAGE", "Salvage"),
                    ("SUPRESS", "Suppress"),
                    ("DESTINY", "Destiny"),
                    ("BARRIER", "Barrier"),
                    ("VENEGANCE", "Venegeance"),
                    ("DELTA_ROCKET", "Delta rocket"),
                    ("LEAP", "Leap"),
                    ("BOND", "Bond"),
                    ("LASER_TURRET", "Laser turret"),
                    ("ALPHA_DRONE", "Alpha drone"),
                    ("SUSPEND", "Suspend"),
                    ("OMEGA_ROCKET", "Omega rocket"),
                    ("REMOTE_BOMB", "Remote bomb"),
                ],
                default="EMP",
                max_length=30,
            ),
        ),
        migrations.AddConstraint(
            model_name="support",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("name", "SANCTUARY"), ("value__lte", 1)),
                    models.Q(
                        (
                            "name__in",
                            [
                                "EMP",
                                "TELEPORT",
                                "RED_STAR_LIFE_EXTENDER",
                                "REMOTE_REPAIR",
                                "TIME_WRAP",
                                "UNITY",
                                "STEALTH",
                                "FORTIFY",
                                "IMPULSE",
                                "ALPHA_ROCKET",
                                "SALVAGE",
                                "SUPRESS",
                                "DESTINY",
                                "BARRIER",
                                "VENEGANCE",
                                "DELTA_ROCKET",
                                "LEAP",
                                "BOND",
                                "LASER_TURRET",
                                "ALPHA_DRONE",
                                "SUSPEND",
                                "OMEGA_ROCKET",
                                "REMOTE_BOMB",
                            ],
                        ),
                        ("value__lte", 12),
                    ),
                    _connector="OR",
                ),
                name="members_support_max_value__gt_1_or_lt_12",
                violation_error_message="For Sanctuary maximum value must be lower than 1, rest attributes must be lower than 12",
            ),
        ),
    ]
