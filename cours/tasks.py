from datetime import datetime, timedelta
from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from cours.models import Course
from users.models import User


@shared_task
def task_send_info_mail(obj_id):

    subject = "Подписка на платформе"
    message = (f"В курс {Course.objects.get(id=obj_id).title},"
               f" на который вы подписаны на нашей платформе были внесены изменения!\n"
               f"Пожалуйста поситите платформу и чтобы ознакомиться с информацией!!!")
    from_email = settings.EMAIL_HOST_USER
    to_email = [Course.objects.get(id=obj_id).user.email]
    send_mail(subject, message, from_email, to_email)


@shared_task
def check_user_last_login():

    if User.objects.all().exists:
        month_ago = datetime.now() - timedelta(days=30)
        for user in User.objects.filter(last_login__lt=month_ago):
            if user.exists:
                user.is_active = False
                user.save()
                print(user.first_name)
            else:
                print(user.email)
    else:
        raise ObjectDoesNotExist("Пользователи не найдены")
