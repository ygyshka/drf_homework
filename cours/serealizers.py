from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from cours.models import Course, Lesson, Pay, Subscription
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
    # subscribe = serializers.SerializerMethodField()

    class Meta:
        model = Course
        # fields = ['title', 'description', 'subscribe', 'user', 'lessons_count', 'lesson']
        fields = ['id', 'title', 'description', 'user', 'lessons_count', 'lesson']

    def get_lessons_count(self, obj):
        return obj.lesson.count()

    # def get_subscribe(self, obj):
    #     return obj.subscription.exists()


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscription
        fields = '__all__'
