# Generated by Django 4.1.7 on 2023-02-22 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_user_id_profile_user'),
        ('member', '0006_otptimeline_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='profile',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
            preserve_default=False,
        ),
    ]
