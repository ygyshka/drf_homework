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
    subscribe = serializers.SerializerMethodField()
    user_now = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'user_now', 'title', 'description', 'subscribe', 'user', 'lessons_count', 'lesson']
        # fields = ['id', 'title', 'description', 'user', 'lessons_count', 'lesson']

    def get_user_now(self, obj):
        return self.context['request'].user.id

    def get_lessons_count(self, obj):
        return obj.lesson.count()

    def get_subscribe(self, obj):

        user = self.context['request'].user
        if user.is_authenticated:
            return obj.subscription.filter(user=user).exists()
        else:
            return False

        # sub = Subscription.objects.get(user=obj.user)
        # print(sub)
        # if self.context['request'].user == sub.user:
        # # if Subscription.objects.filter(user=self.context['request'].user, course=obj) is not None:
        #
        # # if self.context['request'].user.subscribe:
        #     return True
        #
        # return False


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
