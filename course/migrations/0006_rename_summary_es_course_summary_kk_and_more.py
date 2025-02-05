# Generated by Django 4.0.8 on 2024-12-27 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_course_summary_uz_course_title_uz_program_summary_uz_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='summary_es',
            new_name='summary_kk',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='summary_fr',
            new_name='summary_ko',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='title_es',
            new_name='title_kk',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='title_fr',
            new_name='title_ko',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='summary_es',
            new_name='summary_kk',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='summary_fr',
            new_name='summary_ko',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='title_es',
            new_name='title_kk',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='title_fr',
            new_name='title_ko',
        ),
        migrations.RenameField(
            model_name='upload',
            old_name='title_es',
            new_name='title_kk',
        ),
        migrations.RenameField(
            model_name='upload',
            old_name='title_fr',
            new_name='title_ko',
        ),
        migrations.RenameField(
            model_name='uploadvideo',
            old_name='summary_es',
            new_name='summary_kk',
        ),
        migrations.RenameField(
            model_name='uploadvideo',
            old_name='summary_fr',
            new_name='summary_ko',
        ),
        migrations.RenameField(
            model_name='uploadvideo',
            old_name='title_es',
            new_name='title_kk',
        ),
        migrations.RenameField(
            model_name='uploadvideo',
            old_name='title_fr',
            new_name='title_ko',
        ),
        migrations.AddField(
            model_name='course',
            name='summary_tr',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='title_tr',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='program',
            name='summary_tr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='program',
            name='title_tr',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='upload',
            name='title_tr',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='uploadvideo',
            name='summary_tr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadvideo',
            name='title_tr',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
