# Generated by Django 4.0.8 on 2024-12-27 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_newsandevents_summary_uz_newsandevents_title_uz'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsandevents',
            old_name='summary_es',
            new_name='summary_kk',
        ),
        migrations.RenameField(
            model_name='newsandevents',
            old_name='summary_fr',
            new_name='summary_ko',
        ),
        migrations.RenameField(
            model_name='newsandevents',
            old_name='title_es',
            new_name='title_kk',
        ),
        migrations.RenameField(
            model_name='newsandevents',
            old_name='title_fr',
            new_name='title_ko',
        ),
        migrations.AddField(
            model_name='newsandevents',
            name='summary_tr',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='newsandevents',
            name='title_tr',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
