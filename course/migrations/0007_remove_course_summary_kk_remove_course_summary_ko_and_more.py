# Generated by Django 4.0.8 on 2024-12-27 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_rename_summary_es_course_summary_kk_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='summary_kk',
        ),
        migrations.RemoveField(
            model_name='course',
            name='summary_ko',
        ),
        migrations.RemoveField(
            model_name='course',
            name='summary_tr',
        ),
        migrations.RemoveField(
            model_name='course',
            name='title_kk',
        ),
        migrations.RemoveField(
            model_name='course',
            name='title_ko',
        ),
        migrations.RemoveField(
            model_name='course',
            name='title_tr',
        ),
        migrations.RemoveField(
            model_name='program',
            name='summary_kk',
        ),
        migrations.RemoveField(
            model_name='program',
            name='summary_ko',
        ),
        migrations.RemoveField(
            model_name='program',
            name='summary_tr',
        ),
        migrations.RemoveField(
            model_name='program',
            name='title_kk',
        ),
        migrations.RemoveField(
            model_name='program',
            name='title_ko',
        ),
        migrations.RemoveField(
            model_name='program',
            name='title_tr',
        ),
        migrations.RemoveField(
            model_name='upload',
            name='title_kk',
        ),
        migrations.RemoveField(
            model_name='upload',
            name='title_ko',
        ),
        migrations.RemoveField(
            model_name='upload',
            name='title_tr',
        ),
        migrations.RemoveField(
            model_name='uploadvideo',
            name='summary_kk',
        ),
        migrations.RemoveField(
            model_name='uploadvideo',
            name='summary_ko',
        ),
        migrations.RemoveField(
            model_name='uploadvideo',
            name='summary_tr',
        ),
        migrations.RemoveField(
            model_name='uploadvideo',
            name='title_kk',
        ),
        migrations.RemoveField(
            model_name='uploadvideo',
            name='title_ko',
        ),
        migrations.RemoveField(
            model_name='uploadvideo',
            name='title_tr',
        ),
    ]
