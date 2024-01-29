from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='previews/', null=True, blank=True)
    description = models.TextField()

    def str(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='previews/', null=True, blank=True)
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def str(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

# Create your models here.
