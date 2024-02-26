from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import YoutubeLinkValidator
from users.models import User, Payment


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ('id', 'name', 'preview', 'description', 'lessons_count')

    def get_lessons_count(self, instance):
        return instance.lessons.count()

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