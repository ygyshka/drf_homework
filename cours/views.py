from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
# from rest_framework.permissions import IsAuthenticated

from rest_framework.reverse import reverse
# from django.urls import reverse

from cours.models import Course, Lesson, Pay, Subscription
from cours.paginations import NotesPagination
from cours.permissions import IsStaff, IsOwner
from cours.serealizers import CourseSerializer, LessonCreateSerializer, LessonSerializer, PaySerializer, \
    SubscribeSerializer


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = NotesPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [~IsStaff]
        elif self.action == 'destroy':
            permission_classes = [~IsStaff | IsOwner]
        else:
            permission_classes = [IsStaff | IsOwner]
        # permission_classes.append(IsAuthenticated)
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):

    serializer_class = LessonCreateSerializer
    permission_classes = [~IsStaff]

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = NotesPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [~IsStaff | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [~IsStaff | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [~IsStaff | IsOwner]


class PayCreateAPIView(generics.CreateAPIView):

    serializer_class = PaySerializer
    permission_classes = [IsOwner]


class PayListAPIView(generics.ListAPIView):

    serializer_class = PaySerializer
    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson',)
    ordering_fields = ('pay_date',)


class SubscriptionListAPIView(generics.ListAPIView):

    serializer_class = SubscribeSerializer
    queryset = Subscription.objects.all()


def subscribe_in(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.subscribe = True
        course.save()
        return HttpResponseRedirect(reverse('cours:lesson-list'))
    else:
        return HttpResponseRedirect(reverse('cours:lesson-list'))
