# Generated by Django 4.2.5 on 2023-09-07 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0004_alter_post_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="user",
            field=models.ForeignKey(
                default=1694068568.539197,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]