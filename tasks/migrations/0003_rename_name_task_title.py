# Generated by Django 4.1.7 on 2023-04-24 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_rename_end_time_task_end_date_rename_title_task_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='name',
            new_name='title',
        ),
    ]