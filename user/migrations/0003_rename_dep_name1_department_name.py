# Generated by Django 4.2.16 on 2024-11-08 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_name_department_dep_name1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='dep_name1',
            new_name='name',
        ),
    ]
