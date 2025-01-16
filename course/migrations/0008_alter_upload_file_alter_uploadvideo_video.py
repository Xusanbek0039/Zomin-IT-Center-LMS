# Generated by Django 5.0.10 on 2025-01-16 08:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_remove_course_summary_kk_remove_course_summary_ko_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='file',
            field=models.FileField(help_text='Mumkin fayllar: pdf, docx, doc, xls, xlsx, ppt, pptx, zip, rar, 7zip', upload_to='course_files/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])]),
        ),
        migrations.AlterField(
            model_name='uploadvideo',
            name='video',
            field=models.FileField(help_text="Mumkin bo'lgan video formatlar: mp4, mkv, wmv, 3gp, f4v, avi, mp3", upload_to='course_videos/', validators=[django.core.validators.FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])]),
        ),
    ]
