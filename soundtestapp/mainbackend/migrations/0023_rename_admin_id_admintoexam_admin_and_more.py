# Generated by Django 4.0 on 2022-03-03 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainbackend', '0022_filedestination_examinationresult_exam_finished_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admintoexam',
            old_name='admin_id',
            new_name='admin',
        ),
        migrations.RenameField(
            model_name='admintoexam',
            old_name='exam_id',
            new_name='exam',
        ),
    ]
