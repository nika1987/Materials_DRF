from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from materials.models import Course, Lesson
from materials.serliazers import CourseSerializer, LessonSerializer
from users.models import Payment
from users.serliazers import PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    '''READ ALL Courses, Создание'''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonList(generics.ListCreateAPIView):
    '''READ ALL Lessons, Создание'''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save()  # Эта строка сохраняет новый урок в базе данных


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    '''Detail ALL Lessons, Удаление'''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
# Create your views here.


class PaymentListAPIView(generics.ListAPIView):
    '''READ ALL Payments, Добавлена фильтрация'''
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']

