from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from cours.models import Course, Lesson, Pay
from cours.permissions import *
from cours.serealizers import *
    # CourseSerializer, LessonSerializer, PaySerializer


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwnerOrStaff, IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):

    serializer_class = LessonCreateSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class PayCreateAPIView(generics.CreateAPIView):

    serializer_class = PaySerializer


class PayListAPIView(generics.ListAPIView):

    serializer_class = PaySerializer
    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson',)
    ordering_fields = ('pay_date',)
