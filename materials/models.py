from django.conf import settings
from django.db import models

from users.models import User


class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец',
                              null=True, blank=True)
    objects = None
    name = models.CharField(max_length=50)
    preview = models.ImageField(upload_to='previews/', null=True, blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField(null=True, verbose_name='Цена')

    def __str__(self):
        return self.name

    def get_subscribed_users(self):
        subscription_user = [subscription.user for subscription in self.subscribe.all() if
                             subscription.user is not None]
        return subscription_user

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='previews/', null=True, blank=True)
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', null=True,
                              blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    """Подписки"""
    objects = None
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Подписка на курс',
                               related_name='subscribe')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Подписчик')

    is_subscribe = models.BooleanField(default=False, verbose_name="Подписка")

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

# Create your models here.
