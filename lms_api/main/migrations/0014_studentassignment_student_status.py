# Generated by Django 4.2.6 on 2023-12-04 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_rename_studnetassignment_studentassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentassignment',
            name='student_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]