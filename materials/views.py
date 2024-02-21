from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from materials.models import Course, Lesson
from materials.permissions import CustomPermission
from materials.serliazers import CourseSerializer, LessonSerializer
from users.models import Payment
from users.serliazers import PaymentSerializer


class MixinQueryset:
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class CourseViewSet(viewsets.ModelViewSet):
    '''READ ALL Courses, Создание'''
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [CustomPermission]

    def perform_create(self, serializer, send_update_course=None):
        new_course = serializer.save(owner=self.request.user)
        new_course.owner = self.request.user
        new_course.save()
        if new_course:
            send_update_course.delay(new_course.course.id)


class LessonCreateAPIView(generics.CreateAPIView):
    '''CREATE Lesson'''
    serializer_class = LessonSerializer
    permission_classes = [CustomPermission]

    def perform_create(self, serializer, send_update_course=None):
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.owner = self.request.user
        new_lesson.save()
        if new_lesson:
            send_update_course.delay(new_lesson.course.id)


class LessonList(generics.ListCreateAPIView):
    '''READ ALL Lessons, Создание'''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save()  # Эта строка сохраняет новый урок в базе данных


class LessonUpdateAPIView(MixinQueryset, generics.UpdateAPIView):
    '''UPDATE PUT AND PATCH Lesson'''
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_update(self, serializer, send_update_course=None):
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.owner = self.request.user
        new_lesson.save()
        if new_lesson:
            send_update_course.delay(new_lesson.course.id)


class LessonDestroyAPIView(generics.DestroyAPIView):
    '''DELETE Lesson'''
    queryset = Lesson.objects.all()
    permission_classes = [CustomPermission]

# Create your views here.


class PaymentListAPIView(generics.ListAPIView):
    '''READ ALL Payments, Добавлена фильтрация'''
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']

