from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from cours.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@mail.ru',
            is_staff=False,
            is_superuser=True,
        )
        self.user.set_password('test')
        self.user.save()
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.lesson = Lesson(
            title='Тестовый урок',
            description='Описание урока',
            video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            user=self.user,
        )
        self.lesson.save()

        self.course = Course(
            title='Тестовый курс',
            description='Описание курса',
            user=self.user,
        )
        self.course.save()

        self.subscription = Subscription(
            course=self.course,
            user=self.user
        )
        self.subscription.save()

    def test_lesson_create(self):
        """Тестирование создания урока """

        data = {
            'title': self.lesson.title,
            'description': self.lesson.description,
            'video_link': self.lesson.video_link,
            'user': self.lesson.user.id
        }
        response = self.client.post('/lesson/create', data=data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_lesson_delete(self):
        """Тестирование удаления урока """

        response = self.client.delete(f'/lesson/delete/{self.lesson.id}')
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

    def test_lesson_list(self):
        """Тестирование получения списка уроков """

        response = self.client.get(f'/lesson/')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_lesson_retrieve(self):
        """Тестирование получения отдельного урока """

        response = self.client.get(f'/lesson/{self.lesson.id}')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'], self.lesson.title
        )
        self.assertEqual(
            response.data['description'], self.lesson.description
        )

    def test_lesson_update(self):
        """Тестирование обновления урока """

        data = {
            'title': 'Test update',
            'description': 'test update description'
        }
        response = self.client.patch(f'/lesson/update/{self.lesson.id}', data=data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'], data['title']
        )
        self.assertEqual(
            response.data['description'], data['description']
        )

    def test_subscription_create(self):
        """Тестирование создания подписки """

        data = {
            'course': self.course.id,
            'user': self.user.id
        }
        response = self.client.post('/subscription/create', data=data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertTrue(
            Subscription.objects.all().exists()
        )

    def test_subscription_delete(self):
        """Тестирование удаления подписки """

        response = self.client.delete(f'/subscription/delete/{self.subscription.id}')
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

    def test_subscription_update(self):
        """Тестирование обновления подписки """
        
        data = {
            'subscribe': False,
            'course': self.course.id
        }
        response = self.client.patch(f'/subscription/update/{self.subscription.id}', data=data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['course'],  data['course']
        )
        self.assertEqual(
            response.data['subscribe'], data['subscribe']
        )
