# Generated by Django 4.0.8 on 2024-12-27 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_summary_es_newsandevents_summary_kk_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsandevents',
            name='summary_kk',
        ),
        migrations.RemoveField(
            model_name='newsandevents',
            name='summary_ko',
        ),
        migrations.RemoveField(
            model_name='newsandevents',
            name='summary_tr',
        ),
        migrations.RemoveField(
            model_name='newsandevents',
            name='title_kk',
        ),
        migrations.RemoveField(
            model_name='newsandevents',
            name='title_ko',
        ),
        migrations.RemoveField(
            model_name='newsandevents',
            name='title_tr',
        ),
    ]
