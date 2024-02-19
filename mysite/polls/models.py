import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',)
    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    # def get_absolute_url(self):
    #     return reverse("Question_detail", kwargs={"pk": self.pk})


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return self.choice_text

    # def get_absolute_url(self):
    #     return reverse("Choice_detail", kwargs={"pk": self.pk})
