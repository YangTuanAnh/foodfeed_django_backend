# Generated by Django 4.2.4 on 2023-09-13 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_customuser_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile',
            field=models.ForeignKey(default=1694609102.310571, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]