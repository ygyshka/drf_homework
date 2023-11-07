from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from cours.models import Course, Lesson, Pay, Subscription
from cours.paginations import NotesPagination
from cours.permissions import IsStaff, IsOwner
from cours.serealizers import (CourseSerializer, LessonCreateSerializer,
                               LessonSerializer, PaySerializer, SubscribeSerializer)


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


class SubscriptionCreateAPIView(generics.CreateAPIView):

    serializer_class = SubscribeSerializer


class SubscriptionDestroyAPIView(generics.DestroyAPIView):

    queryset = Subscription.objects.all()


# class SubscriptionDUpdateAPIView(generics.UpdateAPIView):    --- был вариант реализовать изменение подписки
# так чтобы была какая то история для пользователей, но не удалось додумать как это сделать,
# вариант с удалением дает то что нужно, насколько я понял задание
#
#     serializer_class = SubscribeSerializer
#     queryset = Subscription.objects.all()
