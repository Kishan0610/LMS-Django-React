# Generated by Django 4.2.6 on 2023-12-05 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_studentassignment_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_img',
            field=models.ImageField(null=True, upload_to='student_profile_imgs/'),
        ),
    ]
