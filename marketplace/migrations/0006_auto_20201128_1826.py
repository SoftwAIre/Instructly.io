# Generated by Django 2.1.7 on 2020-11-28 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0005_user_am_tutor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='am_tutor',
            new_name='is_student',
        ),
        migrations.AddField(
            model_name='user',
            name='is_tutor',
            field=models.BooleanField(default=True),
        ),
    ]