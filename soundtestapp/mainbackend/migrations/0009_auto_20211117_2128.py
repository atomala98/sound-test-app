# Generated by Django 3.2.8 on 2021-11-17 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainbackend', '0008_auto_20211117_2128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='name',
            new_name='name',
        ),
    ]
