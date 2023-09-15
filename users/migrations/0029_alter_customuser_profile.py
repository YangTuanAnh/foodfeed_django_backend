# Generated by Django 4.2.5 on 2023-09-15 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0028_alter_customuser_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="profile",
            field=models.ForeignKey(
                default=1694792040.149855,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
        ),
    ]
