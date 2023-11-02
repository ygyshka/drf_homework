from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from cours.models import Course, Lesson, Pay


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lesson = LessonTitleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'lessons_count', 'lesson']

    def get_lessons_count(self, obj):
        return obj.lesson.count()


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'

