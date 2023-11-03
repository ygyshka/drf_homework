from django.conf import settings
from django.db import models

import constants


# Create your models here.


class Course(models.Model):

    title = models.CharField(max_length=50, verbose_name='название курса')
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **constants.NULLABLE)
    description = models.TextField(verbose_name='описание', **constants.NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **constants.NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):

    title = models.CharField(max_length=50, verbose_name='название урока')
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **constants.NULLABLE)
    description = models.TextField(verbose_name='описание', **constants.NULLABLE)
    video_link = models.CharField(max_length=100, verbose_name='ссылка на видео', **constants.NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **constants.NULLABLE, related_name='lesson')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **constants.NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Pay(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **constants.NULLABLE, related_name='pay')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **constants.NULLABLE, related_name='pay')

    pay_date = models.DateTimeField( verbose_name='дата оплаты')
    pay_amount = models.IntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=70,
                                      verbose_name='способ оплаты',
                                      choices=constants.PAY_METHOD,
                                      **constants.NULLABLE)

    def __str__(self):
        return f'{self.lesson.title if self.lesson.title else self.course.title}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
        # ordering = ['-pay_date']
