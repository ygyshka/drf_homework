from django.db import models

import constants


# Create your models here.


class Course(models.Model):

    title = models.CharField(max_length=50, verbose_name='название курса')
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **constants.NULLABLE)
    description = models.TextField(verbose_name='описание', **constants.NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):

    title = models.CharField(max_length=50, verbose_name='название урока')
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **constants.NULLABLE)
    description = models.TextField(verbose_name='описание', **constants.NULLABLE)
    video_link = models.CharField(max_length=100, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **constants.NULLABLE, related_name='lesson')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
