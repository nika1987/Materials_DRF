from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet
from materials.views import LessonList, LessonDetail

app_name = MaterialsConfig.name
router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonList.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetail.as_view(), name='lesson-detail'),
]
