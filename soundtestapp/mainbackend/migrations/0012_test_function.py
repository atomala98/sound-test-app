# Generated by Django 3.2.8 on 2021-11-30 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbackend', '0011_exam_test_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='function',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]