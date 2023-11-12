from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from cours.models import Course, Lesson, Pay, Subscription
from cours.servises import pay_link
from cours.validators import LinkValid


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValid(field='video_link')]


class LessonTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lesson = LessonTitleSerializer(many=True, read_only=True)
    subscribe = serializers.SerializerMethodField()
    user_now = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'user_now', 'title', 'description', 'subscribe', 'user', 'lessons_count', 'lesson']


    def get_user_now(self, obj):
        return self.context['request'].user.email

    def get_lessons_count(self, obj):
        return obj.lesson.count()

    def get_subscribe(self, obj):

        user = self.context['request'].user
        if user.is_authenticated:
            try:
                subscription = obj.subscription.get(user=user)
                print(subscription.__dict__)
                return subscription.subscribe
            except ObjectDoesNotExist:
                return False


class PaySerializer(serializers.ModelSerializer):

    pay_link = serializers.SerializerMethodField()

    class Meta:
        model = Pay
        fields = '__all__'

    def get_pay_link(self, obj):
        try:
            if obj.course:
                title = obj.course.title
                pay_amount = obj.pay_amount
                return pay_link(title, pay_amount)

        except ObjectDoesNotExist:

            return ""

class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
