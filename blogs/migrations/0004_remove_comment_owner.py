# Generated by Django 3.1 on 2020-08-11 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='owner',
        ),
    ]
