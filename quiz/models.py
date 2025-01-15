import json
import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import (
    MaxValueValidator,
    validate_comma_separated_integer_list,
)
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from model_utils.managers import InheritanceManager

from course.models import Course
from core.utils import unique_slug_generator

CHOICE_ORDER_OPTIONS = (
    ("content", _("Tarkib bilan")),
    ("random", _("Aralash ")),
    ("none", _("Nomalum")),
)

CATEGORY_OPTIONS = (
    ("assignment", _("Topshiriq")),
    ("exam", _("Imtihon")),
    ("practice", _("Amaliy viktorina")),
)


class QuizManager(models.Manager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query:
            or_lookup = (
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(category__icontains=query)
                | Q(slug__icontains=query)
            )
            queryset = queryset.filter(or_lookup).distinct()
        return queryset


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("Nom"), max_length=60)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(
        verbose_name=_("Tavsif"),
        blank=True,
        help_text=_("Viktorinaning batafsil tavsifi"),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_OPTIONS, blank=True)
    random_order = models.BooleanField(
        default=False,
        verbose_name=_("Tasodifiy"),
        help_text=_("Savollarni tasodifiy tartibda yoki belgilangan tartibda ko'rsatingmi?"),
    )
    answers_at_end = models.BooleanField(
        default=False,
        verbose_name=_("Javoblar oxirida"),
        help_text=_(
            "To'g'ri javob savoldan keyin ko'rsatilmaydi. Javoblar oxirida ko'rsatiladi."
        ),
    )
    exam_paper = models.BooleanField(
        default=False,
        verbose_name=_("Imtihon qog'ozi"),
        help_text=_(
            "Ha bo'lsa, foydalanuvchining har bir urinish natijasi saqlanadi. Belgilash uchun zarur."
        ),
    )
    single_attempt = models.BooleanField(
        default=False,
        verbose_name=_("Yagona urinish"),
        help_text=_("Ha bo'lsa, foydalanuvchining faqat bitta urinishiga ruxsat beriladi."),
    )
    pass_mark = models.SmallIntegerField(
        default=50,
        verbose_name=_("O'tish belgisi"),
        validators=[MaxValueValidator(100)],
        help_text=_("Imtihondan o'tish uchun talab qilinadigan foiz."),
    )
    draft = models.BooleanField(
        default=False,
        verbose_name=_("Qoralama"),
        help_text=_(
            "Ha bo'lsa, viktorina viktorina ro'yxatida ko'rsatilmaydi va uni faqat viktorinalarni tahrir qila oladigan foydalanuvchilar olishi mumkin."
        ),
    )
    timestamp = models.DateTimeField(auto_now=True)

    objects = QuizManager()

    class Meta:
        verbose_name = _("Viktorina")
        verbose_name_plural = _("Viktorinalar")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.single_attempt:
            self.exam_paper = True

        if not (0 <= self.pass_mark <= 100):
            raise ValidationError(_("O'tish belgisi 0 dan 100 gacha bo'lishi kerak."))

        super().save(*args, **kwargs)

    def get_questions(self):
        return self.question_set.all().select_subclasses()

    @property
    def get_max_score(self):
        return self.get_questions().count()

    def get_absolute_url(self):
        return reverse("quiz_index", kwargs={"slug": self.course.slug})


@receiver(pre_save, sender=Quiz)
def quiz_pre_save_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class ProgressManager(models.Manager):
    def new_progress(self, user):
        new_progress = self.create(user=user, score="")
        return new_progress


class Progress(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_("Foydalanuvchi"), on_delete=models.CASCADE
    )
    score = models.CharField(
        max_length=1024,
        verbose_name=_("Natija"),
        validators=[validate_comma_separated_integer_list],
    )

    objects = ProgressManager()

    class Meta:
        verbose_name = _("Foydalanuvchi yo'nalishi")
        verbose_name_plural = _("Foydalanuvchi yo'nalishi natijasi")

    def list_all_cat_scores(self):
        return {}  # Implement as needed

    def update_score(self, question, score_to_add=0, possible_to_add=0):
        if not isinstance(score_to_add, int) or not isinstance(possible_to_add, int):
            return _("Xatolik"), _("Ballar qiymatlari noto‘g‘ri.")

        to_find = re.escape(str(question.quiz)) + r",(?P<score>\d+),(?P<possible>\d+),"
        match = re.search(to_find, self.score, re.IGNORECASE)

        if match:
            updated_score = int(match.group("score")) + abs(score_to_add)
            updated_possible = int(match.group("possible")) + abs(possible_to_add)
            new_score = ",".join(
                [str(question.quiz), str(updated_score), str(updated_possible), ""]
            )
            self.score = self.score.replace(match.group(), new_score)
            self.save()
        else:
            self.score += ",".join(
                [str(question.quiz), str(score_to_add), str(possible_to_add), ""]
            )
            self.save()

    def show_exams(self):
        if self.user.is_superuser:
            return Sitting.objects.filter(complete=True).order_by("-end")
        else:
            return Sitting.objects.filter(user=self.user, complete=True).order_by(
                "-end"
            )


class SittingManager(models.Manager):
    def new_sitting(self, user, quiz, course):
        if quiz.random_order:
            question_set = quiz.question_set.all().select_subclasses().order_by("?")
        else:
            question_set = quiz.question_set.all().select_subclasses()

        question_ids = [item.id for item in question_set]
        if not question_ids:
            raise ImproperlyConfigured(
                _(
                    "Viktorinaning savollar to'plami bo'sh. Iltimos, savollarni to'g'ri sozlang."
                )
            )

        questions = ",".join(map(str, question_ids)) + ","

        new_sitting = self.create(
            user=user,
            quiz=quiz,
            course=course,
            question_order=questions,
            question_list=questions,
            incorrect_questions="",
            current_score=0,
            complete=False,
            user_answers="{}",
        )
        return new_sitting

    def user_sitting(self, user, quiz, course):
        if (
            quiz.single_attempt
            and self.filter(user=user, quiz=quiz, course=course, complete=True).exists()
        ):
            return False
        try:
            sitting = self.get(user=user, quiz=quiz, course=course, complete=False)
        except Sitting.DoesNotExist:
            sitting = self.new_sitting(user, quiz, course)
        except Sitting.MultipleObjectsReturned:
            sitting = self.filter(
                user=user, quiz=quiz, course=course, complete=False
            ).first()
        return sitting


class Sitting(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("Foydalanuvchi"), on_delete=models.CASCADE
    )
    quiz = models.ForeignKey(Quiz, verbose_name=_("Viktorena"), on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, verbose_name=_("Kurs"), on_delete=models.CASCADE
    )
    question_order = models.CharField(
        max_length=1024,
        verbose_name=_("Savol berish tartibi"),
        validators=[validate_comma_separated_integer_list],
    )
    question_list = models.CharField(
        max_length=1024,
        verbose_name=_("Savollar ro'yxati"),
        validators=[validate_comma_separated_integer_list],
    )
    incorrect_questions = models.CharField(
        max_length=1024,
        blank=True,
        verbose_name=_("Noto'g'ri savollar"),
        validators=[validate_comma_separated_integer_list],
    )
    current_score = models.IntegerField(verbose_name=_("Joriy ball"))
    complete = models.BooleanField(default=False, verbose_name=_("Bajarildi"))
    user_answers = models.TextField(
        blank=True, default="{}", verbose_name=_("Foydalanuvchi javoblari")
    )
    start = models.DateTimeField(auto_now_add=True, verbose_name=_("Boshlash"))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_("Tugatish"))

    objects = SittingManager()

    class Meta:
        permissions = (("view_sittings", _("Tugallangan imtihonlarni ko'rish mumkin.")),)

    def get_first_question(self):
        if not self.question_list:
            return False
        first_question_id = int(self.question_list.split(",", 1)[0])
        return Question.objects.get_subclass(id=first_question_id)

    def remove_first_question(self):
        if not self.question_list:
            return
        _, remaining_questions = self.question_list.split(",", 1)
        self.question_list = remaining_questions
        self.save()

    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    @property
    def get_current_score(self):
        return self.current_score

    def _question_ids(self):
        return [int(q) for q in self.question_order.split(",") if q]

    @property
    def get_percent_correct(self):
        total_questions = len(self._question_ids())
        if total_questions == 0:
            return 0
        percent = (self.current_score / total_questions) * 100
        return min(max(int(round(percent)), 0), 100)

    def mark_quiz_complete(self):
        self.complete = True
        self.end = now()
        self.save()

    def add_incorrect_question(self, question):
        incorrect_ids = self.get_incorrect_questions
        incorrect_ids.append(question.id)
        self.incorrect_questions = ",".join(map(str, incorrect_ids)) + ","
        if self.complete:
            self.add_to_score(-1)
        self.save()

    @property
    def get_incorrect_questions(self):
        return [int(q) for q in self.incorrect_questions.split(",") if q]

    def remove_incorrect_question(self, question):
        incorrect_ids = self.get_incorrect_questions
        if question.id in incorrect_ids:
            incorrect_ids.remove(question.id)
            self.incorrect_questions = ",".join(map(str, incorrect_ids)) + ","
            self.add_to_score(1)
            self.save()

    @property
    def check_if_passed(self):
        return self.get_percent_correct >= self.quiz.pass_mark

    @property
    def result_message(self):
        if self.check_if_passed:
            return _("Siz ushbu viktorinadan o'tdingiz, tabriklaymiz!")
        else:
            return _("Bu testda muvaffaqiyatsiz boʻldingiz, qayta urinib koʻring.")

    def add_user_answer(self, question, guess):
        user_answers = json.loads(self.user_answers)
        user_answers[str(question.id)] = guess
        self.user_answers = json.dumps(user_answers)
        self.save()

    def get_questions(self, with_answers=False):
        question_ids = self._question_ids()
        questions = sorted(
            self.quiz.question_set.filter(id__in=question_ids).select_subclasses(),
            key=lambda q: question_ids.index(q.id),
        )
        if with_answers:
            user_answers = json.loads(self.user_answers)
            for question in questions:
                question.user_answer = user_answers.get(str(question.id))
        return questions

    @property
    def questions_with_user_answers(self):
        return {q: q.user_answer for q in self.get_questions(with_answers=True)}

    @property
    def get_max_score(self):
        return len(self._question_ids())

    def progress(self):
        answered = len(json.loads(self.user_answers))
        total = self.get_max_score
        return answered, total


class Question(models.Model):
    quiz = models.ManyToManyField(Quiz, verbose_name=_("Viktorina"), blank=True)
    figure = models.ImageField(
        upload_to="uploads/%Y/%m/%d",
        blank=True,
        verbose_name=_("Rasm"),
        help_text=_("Agar kerak bo'lsa, savol uchun rasm qo'shing."),
    )
    content = models.CharField(
        max_length=1000,
        help_text=_("Ko'rsatilishini xohlagan savol matnini kiriting"),
        verbose_name=_("Savol"),
    )
    explanation = models.TextField(
        max_length=2000,
        blank=True,
        help_text=_("Savolga javob berilgandan keyin tushuntirish ko'rsatiladi."),
        verbose_name=_("Tushuntirish"),
    )

    objects = InheritanceManager()

    class Meta:
        verbose_name = _("Savol")
        verbose_name_plural = _("Savollar")

    def __str__(self):
        return self.content


class MCQuestion(Question):
    choice_order = models.CharField(
        max_length=30,
        choices=CHOICE_ORDER_OPTIONS,
        blank=True,
        help_text=_(
            "Ko'p tanlovli variantlar foydalanuvchiga ko'rsatiladigan tartib"
        ),
        verbose_name=_("Tanlov tartibi"),
    )

    class Meta:
        verbose_name = _("Ko'p tanlovli savol")
        verbose_name_plural = _("Ko'p tanlovli savollar")

    def check_if_correct(self, guess):
        try:
            answer = Choice.objects.get(id=int(guess))
            return answer.correct
        except (Choice.DoesNotExist, ValueError):
            return False

    def order_choices(self, queryset):
        if self.choice_order == "content":
            return queryset.order_by("choice_text")
        elif self.choice_order == "random":
            return queryset.order_by("?")
        else:
            return queryset

    def get_choices(self):
        return self.order_choices(Choice.objects.filter(question=self))

    def get_choices_list(self):
        return [(choice.id, choice.choice_text) for choice in self.get_choices()]

    def answer_choice_to_string(self, guess):
        try:
            return Choice.objects.get(id=int(guess)).choice_text
        except (Choice.DoesNotExist, ValueError):
            return ""


class Choice(models.Model):
    question = models.ForeignKey(
        MCQuestion, verbose_name=_("Savol"), on_delete=models.CASCADE
    )
    choice_text = models.CharField(
        max_length=1000,
        help_text=_("Ko'rsatmoqchi bo'lgan tanlov matnini kiriting"),
        verbose_name=_("Tarkib"),
    )
    correct = models.BooleanField(
        default=False,
        help_text=_("Bu to'g'ri javobmi?"),
        verbose_name=_("To'g'ri"),
    )

    class Meta:
        verbose_name = _("Tanlov")
        verbose_name_plural = _("Tanlovlar")

    def __str__(self):
        return self.choice_text


class EssayQuestion(Question):
    class Meta:
        verbose_name = _("Insho uslubiga oid savol")
        verbose_name_plural = _("Insho uslubiga oid savollar")

    def check_if_correct(self, guess):
        return False  # Needs manual grading

    def get_answers(self):
        return False

    def get_answers_list(self):
        return False

    def answer_choice_to_string(self, guess):
        return str(guess)
