# Generated by Django 4.0.8 on 2024-12-27 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='default.gif', null=True, upload_to='profile_pictures/%y/%m/%d/'),
        ),
    ]
