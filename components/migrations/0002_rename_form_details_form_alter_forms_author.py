# Generated by Django 4.0.4 on 2022-12-02 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('components', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='details',
            old_name='Form',
            new_name='form',
        ),
        migrations.AlterField(
            model_name='forms',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]