# Generated by Django 5.0.6 on 2024-10-28 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='handbuch_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]