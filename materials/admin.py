#from django.contrib import admin

from django.contrib import admin
from materials.models import Course, Subscription, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'course')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'course')
