from rest_framework import viewsets, generics, status, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import CoursePagination
from materials.permissions import IsModer, IsOwner
from materials.serliazers import (
    CourseSerializer, LessonSerializer,
    SubscriptionSerializer)
from materials.tasks import send_update_course


class CourseViewSet(viewsets.ModelViewSet):
    """READ ALL Courses, Создание"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePagination

    def perform_update(self, serializer):
        updated_course = serializer.save()
        if updated_course:
            send_update_course.delay(updated_course.id)

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ('update', 'retrieve',):
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """CREATE Lesson"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.owner = self.request.user
        new_lesson.save()
        if new_lesson:
            send_update_course.delay(new_lesson.course.id)


class LessonListAPIView(generics.ListCreateAPIView):
    """READ ALL Lessons, Создание"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save()  # Эта строка сохраняет новый урок в базе данных


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """READ ONE Lesson"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, IsModer]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """UPDATE PUT AND PATCH Lesson"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]

    def perform_update(self, serializer):
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.owner = self.request.user
        new_lesson.save()
        if new_lesson:
            send_update_course.delay(new_lesson.course.id)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """DELETE Lesson"""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    # Create your views here.

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.data = None
        self.user = None

    def post(self, request, *args, **kwargs):
        user = self.user
        course_id = self.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        print(subscription)
        if not created:
            subscription.delete()
            message = 'Subscription removed'
        else:
            message = 'Subscription added'

        return Response({"message": message}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user = self.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def post(self, request, *args, **kwargs):
        user = self.request.user

        course_id = request.data.get('course_id')
        course = course_id.objects.get_object_or_404()

        subscription = Subscription.objects.filter(owner=user, course=course, is_active=True)

        if user != subscription.owner:
            raise serializers.ValidationError('Нельзя удалить чужую подписку!')
        else:
            if subscription.exists():
                subscription.delete()
                message = 'подписка удалена'

            else:
                Subscription.objects.create(owner=user, course=course, is_active=True)
                message = 'подписка добавлена'

            return Response({"message": message}, {'user': user})

    def perform_create(self, serializer):
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.save()

    def patch(self, request, *args, **kwargs):

        instance = self.get_object()

        subscribed_users = instance.get_subscribed_users()

        # Отправляем уведомление каждому подписанному пользователю

        for user in subscribed_users:

            if user.email:
                send_update_course.delay(user.email, instance.name)

        return super().request(*args, **kwargs)
