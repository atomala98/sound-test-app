# Generated by Django 4.0 on 2022-04-04 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbackend', '0031_examtest_parameter_3_examtest_parameter_4_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileset',
            name='filename_list',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]