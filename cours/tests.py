from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from cours.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@mail.ru',
            password='test',
            is_staff=True,
            is_superuser=True,
        )
        self.user.save()
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer'+self.access_token)

        self.lesson = Lesson(
            title='Тестовый урок',
            description='Описание урока',
            video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            user=self.user,
        )

    # def test_create_course(self):
    #     """ Тестирование создания курса """
    #
    #     data = {
    #         'title': 'Тестовый курс',
    #         'description': 'Описание курса'
    #     }
    #
    #     response = self.client.post(
    #         '/cours/',
    #         data=data
    #     )
    #     print(response.json())
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_201_CREATED)
    #
    #     self.assertEqual(
    #         response.json(),
    #         {'title': 'Тестовый курс', 'description': 'Описание курса', 'lessons_count': 0, 'lesson': []}
    #     )
    #
    #     self.assertTrue(
    #         Course.objects.all().exists()
    #     )

    def test_lesson_create(self):
        """Тестирование создания урока """

        data = {
            'title': 'Тестовый урок',
            'description': 'Описание урока',
            'video_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }
        print(self.lesson)
        response = self.client.post(
            '/lesson/create',
            data=data
            # data=...
        )
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED)
