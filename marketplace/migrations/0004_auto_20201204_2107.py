# Generated by Django 2.1.7 on 2020-12-04 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0003_listing_session_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tag_line',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='tutoring_time',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2),
        ),
    ]