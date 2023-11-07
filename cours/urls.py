from django.urls import path
from rest_framework.routers import DefaultRouter
from cours.apps import CoursConfig
from cours.views import (CourseViewSet, LessonCreateAPIView,
                         LessonListAPIView, LessonRetrieveAPIView,
                         LessonUpdateAPIView, LessonDestroyAPIView,
                         PayCreateAPIView, PayListAPIView,
                         SubscriptionListAPIView, subscribe_in)

app_name = CoursConfig.name

router = DefaultRouter()
router.register(r'cours', CourseViewSet, basename=app_name)

urlpatterns = [
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson-crete'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    # pay
    path('pay/create/', PayCreateAPIView.as_view(), name='pay-create'),
    path('pay/', PayListAPIView.as_view(), name='pay-list'),
    # subscription
    path('subscription/create/', subscribe_in, name='subscription-create'),
    path('subscription/', SubscriptionListAPIView.as_view(), name='subscription-list'),

] + router.urls
