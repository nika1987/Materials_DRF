from rest_framework import viewsets, generics, status, serializers

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription, CoursePayment
from materials.paginators import CoursePagination
from materials.permissions import IsModer, IsOwner
from materials.serliazers import (
    CourseSerializer, LessonSerializer,
    SubscriptionSerializer, CoursePaymentSerializer)
from materials.services import get_session, create_stripe_price, create_stripe_session
from users.models import Payment


class CourseViewSet(viewsets.ModelViewSet):
    '''READ ALL Courses, Создание'''
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePagination

    def perform_create(self, serializer, send_update_course=None):
        new_course = serializer.save(owner=self.request.user)
        new_course.owner = self.request.user
        new_course.save()
        if new_course:
            send_update_course.delay(new_course.course.id)

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ('update', 'retrieve',):
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()


class CoursePaymentApiView(generics.CreateAPIView):
    queryset = CoursePayment.objects.all()
    serializer_class = CoursePaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        paid_of_course = serializer.save()
        payment_link = get_session(paid_of_course)
        paid_of_course.payment_link = payment_link
        paid_of_course.save()


class CoursePaymentApiView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CoursePaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.validated_data.get('name')
        if not course:
            raise serializers.ValidationError('Укажите курс')

        payment = serializer.save()
        stripe_price_id = create_stripe_price(payment)
        payment.payment_link, payment.payment_id = create_stripe_session(stripe_price_id)
        payment.save()


class LessonCreateAPIView(generics.CreateAPIView):
    '''CREATE Lesson'''
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer, send_update_course=None):
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.owner = self.request.user
        new_lesson.save()
        if new_lesson:
            send_update_course.delay(new_lesson.course.id)


class LessonListAPIView(generics.ListCreateAPIView):
    '''READ ALL Lessons, Создание'''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save()  # Эта строка сохраняет новый урок в базе данных


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    '''READ ONE Lesson'''
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, IsModer]


class LessonUpdateAPIView(generics.UpdateAPIView):
    '''UPDATE PUT AND PATCH Lesson'''
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]

    def perform_update(self, serializer, send_update_course=None):
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.owner = self.request.user
        new_lesson.save()
        if new_lesson:
            send_update_course.delay(new_lesson.course.id)


class LessonDestroyAPIView(generics.DestroyAPIView):
    '''DELETE Lesson'''
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


# Create your views here.


class SubscriptionAPIView(APIView):
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        print(subscription)
        if not created:
            subscription.delete()
            message = 'Subscription removed'
        else:
            message = 'Subscription added'

        return Response({"message": message}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
