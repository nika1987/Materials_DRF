from rest_framework import serializers
from materials.models import Course, Lesson
from users.models import User, Payment


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'preview', 'description', 'lessons_count')

    def get_lessons_count(self, instance):
        return instance.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
