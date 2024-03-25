from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import YoutubeLinkValidator


#def get_lessons_count(instance):
#    return instance.lessons.count()


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
# Создания поля для подсчета уроков
#    lessons_count = serializers.SerializerMethodField()

    lessons_count = SerializerMethodField()
#    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj.pk).count()

    class Meta:
        model = Course
        fields = ('id', 'name', 'preview', 'description', 'lessons_count', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(course=obj, user=user).exists()
        return False


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[YoutubeLinkValidator(field='video_link')])

    class Meta:
        model = Lesson
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
