# Generated by Django 5.0.10 on 2025-01-16 08:53

import django.core.validators
import django.db.models.deletion
import re
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_alter_upload_file_alter_uploadvideo_video'),
        ('quiz', '0007_remove_choice_choice_text_kk_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'verbose_name': 'Tanlov', 'verbose_name_plural': 'Tanlovlar'},
        ),
        migrations.AlterModelOptions(
            name='essayquestion',
            options={'verbose_name': 'Insho uslubiga oid savol', 'verbose_name_plural': 'Insho uslubiga oid savollar'},
        ),
        migrations.AlterModelOptions(
            name='mcquestion',
            options={'verbose_name': "Ko'p tanlovli savol", 'verbose_name_plural': "Ko'p tanlovli savollar"},
        ),
        migrations.AlterModelOptions(
            name='progress',
            options={'verbose_name': "Foydalanuvchi yo'nalishi", 'verbose_name_plural': "Foydalanuvchi yo'nalishi natijasi"},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Savol', 'verbose_name_plural': 'Savollar'},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name': 'Viktorina', 'verbose_name_plural': 'Viktorinalar'},
        ),
        migrations.AlterModelOptions(
            name='sitting',
            options={'permissions': (('view_sittings', "Tugallangan imtihonlarni ko'rish mumkin."),)},
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(help_text="Ko'rsatmoqchi bo'lgan tanlov matnini kiriting", max_length=1000, verbose_name='Tarkib'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_text_en',
            field=models.CharField(help_text="Ko'rsatmoqchi bo'lgan tanlov matnini kiriting", max_length=1000, null=True, verbose_name='Tarkib'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_text_ru',
            field=models.CharField(help_text="Ko'rsatmoqchi bo'lgan tanlov matnini kiriting", max_length=1000, null=True, verbose_name='Tarkib'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_text_uz',
            field=models.CharField(help_text="Ko'rsatmoqchi bo'lgan tanlov matnini kiriting", max_length=1000, null=True, verbose_name='Tarkib'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='correct',
            field=models.BooleanField(default=False, help_text="Bu to'g'ri javobmi?", verbose_name="To'g'ri"),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.mcquestion', verbose_name='Savol'),
        ),
        migrations.AlterField(
            model_name='mcquestion',
            name='choice_order',
            field=models.CharField(blank=True, choices=[('content', 'Tarkib bilan'), ('random', 'Aralash '), ('none', 'Nomalum')], help_text="Ko'p tanlovli variantlar foydalanuvchiga ko'rsatiladigan tartib", max_length=30, verbose_name='Tanlov tartibi'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='score',
            field=models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Natija'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Foydalanuvchi'),
        ),
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.CharField(help_text="Ko'rsatilishini xohlagan savol matnini kiriting", max_length=1000, verbose_name='Savol'),
        ),
        migrations.AlterField(
            model_name='question',
            name='content_en',
            field=models.CharField(help_text="Ko'rsatilishini xohlagan savol matnini kiriting", max_length=1000, null=True, verbose_name='Savol'),
        ),
        migrations.AlterField(
            model_name='question',
            name='content_ru',
            field=models.CharField(help_text="Ko'rsatilishini xohlagan savol matnini kiriting", max_length=1000, null=True, verbose_name='Savol'),
        ),
        migrations.AlterField(
            model_name='question',
            name='content_uz',
            field=models.CharField(help_text="Ko'rsatilishini xohlagan savol matnini kiriting", max_length=1000, null=True, verbose_name='Savol'),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=models.TextField(blank=True, help_text="Savolga javob berilgandan keyin tushuntirish ko'rsatiladi.", max_length=2000, verbose_name='Tushuntirish'),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation_en',
            field=models.TextField(blank=True, help_text="Savolga javob berilgandan keyin tushuntirish ko'rsatiladi.", max_length=2000, null=True, verbose_name='Tushuntirish'),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation_ru',
            field=models.TextField(blank=True, help_text="Savolga javob berilgandan keyin tushuntirish ko'rsatiladi.", max_length=2000, null=True, verbose_name='Tushuntirish'),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation_uz',
            field=models.TextField(blank=True, help_text="Savolga javob berilgandan keyin tushuntirish ko'rsatiladi.", max_length=2000, null=True, verbose_name='Tushuntirish'),
        ),
        migrations.AlterField(
            model_name='question',
            name='figure',
            field=models.ImageField(blank=True, help_text="Agar kerak bo'lsa, savol uchun rasm qo'shing.", upload_to='uploads/%Y/%m/%d', verbose_name='Rasm'),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ManyToManyField(blank=True, to='quiz.quiz', verbose_name='Viktorina'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='answers_at_end',
            field=models.BooleanField(default=False, help_text="To'g'ri javob savoldan keyin ko'rsatilmaydi. Javoblar oxirida ko'rsatiladi.", verbose_name='Javoblar oxirida'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='category',
            field=models.CharField(blank=True, choices=[('assignment', 'Topshiriq'), ('exam', 'Imtihon'), ('practice', 'Amaliy viktorina')], max_length=20),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.TextField(blank=True, help_text='Viktorinaning batafsil tavsifi', verbose_name='Tavsif'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description_en',
            field=models.TextField(blank=True, help_text='Viktorinaning batafsil tavsifi', null=True, verbose_name='Tavsif'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description_ru',
            field=models.TextField(blank=True, help_text='Viktorinaning batafsil tavsifi', null=True, verbose_name='Tavsif'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description_uz',
            field=models.TextField(blank=True, help_text='Viktorinaning batafsil tavsifi', null=True, verbose_name='Tavsif'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='draft',
            field=models.BooleanField(default=False, help_text="Ha bo'lsa, viktorina viktorina ro'yxatida ko'rsatilmaydi va uni faqat viktorinalarni tahrir qila oladigan foydalanuvchilar olishi mumkin.", verbose_name='Qoralama'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='exam_paper',
            field=models.BooleanField(default=False, help_text="Ha bo'lsa, foydalanuvchining har bir urinish natijasi saqlanadi. Belgilash uchun zarur.", verbose_name="Imtihon qog'ozi"),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='pass_mark',
            field=models.SmallIntegerField(default=50, help_text="Imtihondan o'tish uchun talab qilinadigan foiz.", validators=[django.core.validators.MaxValueValidator(100)], verbose_name="O'tish belgisi"),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='random_order',
            field=models.BooleanField(default=False, help_text="Savollarni tasodifiy tartibda yoki belgilangan tartibda ko'rsatingmi?", verbose_name='Tasodifiy'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='single_attempt',
            field=models.BooleanField(default=False, help_text="Ha bo'lsa, foydalanuvchining faqat bitta urinishiga ruxsat beriladi.", verbose_name='Yagona urinish'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=60, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title_en',
            field=models.CharField(max_length=60, null=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title_ru',
            field=models.CharField(max_length=60, null=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title_uz',
            field=models.CharField(max_length=60, null=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='complete',
            field=models.BooleanField(default=False, verbose_name='Bajarildi'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course', verbose_name='Kurs'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='current_score',
            field=models.IntegerField(verbose_name='Joriy ball'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Tugatish'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='incorrect_questions',
            field=models.CharField(blank=True, max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name="Noto'g'ri savollar"),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='question_list',
            field=models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name="Savollar ro'yxati"),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='question_order',
            field=models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Savol berish tartibi'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz', verbose_name='Viktorena'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='start',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Boshlash'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Foydalanuvchi'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='user_answers',
            field=models.TextField(blank=True, default='{}', verbose_name='Foydalanuvchi javoblari'),
        ),
    ]
