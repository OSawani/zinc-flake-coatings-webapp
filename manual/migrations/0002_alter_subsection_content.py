# Generated by Django 5.0.6 on 2024-06-13 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manual', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsection',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
