from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from materials.models import Course, Lesson, Subscription
from users.models import User


'''LESSONS TESTS'''
# ---------------------------------------------------------------


class EducationTestCase(APITestCase):
    '''Тест моделей Course и Lesson'''

    def setUp(self) -> None:
        '''Создается тестовый пользователь'''
        self.group = Group.objects.create(name='moderator')

        self.user = User.objects.create_superuser(
            email='test@mail.ru', password='555test555'
        )
        self.user.groups.add(self.group)
        self.user.save()

        self.client.force_authenticate(user=self.user)

        '''Создается тестовый курс'''
        self.course = Course.objects.create(
            name='test course',
            description='test course description'
        )

        '''Создается тестовый урок'''
        self.lesson = Lesson.objects.create(
            name='test lesson',
            description='test lesson description',
            video_link='https://www.youtube.com/',
            course=self.course,
            owner=self.user
        )

    def test_list_lesson(self):
        '''Тест READ LIST lesson'''

        response = self.client.get(
            '/lesson/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        print(response.json())

        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).name,
            response.json()[0].get('name'))

    def test_retrieve_lesson(self):
        '''Тест READ ONE lesson'''
        response = self.client.get(f'/lesson/{self.lesson.pk}/')
        print(response.json())

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )

        response = response.json()

        self.assertEqual(response.get('name'), 'test lesson')
        self.assertEqual(response.get('preview'), None)
        self.assertEqual(response.get('description'), 'test lesson description')
        self.assertEqual(response.get('video_link'), 'https://www.youtube.com/')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('owner'), self.user.pk)

    def test_create_lesson(self):
        '''Тест CREATE lesson'''

        data = {
            'name': 'test lesson 2',
            'description': 'description 2',
            'video_link': 'https://www.youtube.com/',
            'course': self.course.pk,
            'owner': self.user.pk,
        }
        self.user.groups.remove(self.group)

        lesson_create_url = reverse('materials:lesson_create')
        response = self.client.post(lesson_create_url, data=data)
        print(self.user.groups)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.json().get('name'),
            data.get('name')
        )

        self.assertTrue(
            Lesson.objects.get(pk=self.lesson.pk).name,
            data.get('name')
        )

    def test_update_lesson(self):
        '''Тест UPDATE lesson'''

        data = {
            'name': 'updated lesson',
            'description': 'updated description',
            'video_link': 'https://www.youtube.com/',
            'course': self.course.pk
        }

        response = self.client.put(
            f'/lesson/update/{self.lesson.pk}/', data=data,
        )

        print(response.json())

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('name'), 'updated lesson')
        self.assertEqual(response.get('description'), 'updated description')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('owner'), self.user.pk)

    def test_delete_lesson(self):
        '''Тест DELETE lesson'''

        response = self.client.delete(
            f'/lesson/delete/{self.lesson.pk}/',
        )

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.all().exists(),
        )


'''SUBSCRIPTION TESTS'''
# ----------------------------------------------------------------


class SubscriptionTestCase(APITestCase):
    ''''Тест модели Subscription'''
    def setUp(self) -> None:
        ''''Создается тестовый пользователь'''
        self.user = User.objects.create_superuser(
            email='test2@mail.ru', password='777test777'
        )
        self.client.force_authenticate(user=self.user)

        self.second_user = User.objects.create_user(
            email='test@yandex.ru', password='supertestuser88')

        '''Создается тестовый курс'''
        self.course = Course.objects.create(
            name='test course sub',
            description='test desc sub'
        )

        self.second_course = Course.objects.create(
            name='test second course sub',
            description='test second desc sub'
        )


        '''Создание подписки'''
        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            is_subscribe=True
        )

    def test_create_subscription(self):
        '''Тест CREATE Subscription'''

        data = {
            'user': self.second_user.pk,
            'course_id': self.second_course.pk,
        }

        subscription_url = reverse('materials:subscription')

        response = self.client.post(subscription_url, data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Subscription.objects.all().count(), 2)

    def test_list_subscription(self):
        '''Тест LIST Subscription'''
        subscription_url = reverse('materials:subscription')
        print(subscription_url)
        response = self.client.get(subscription_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
