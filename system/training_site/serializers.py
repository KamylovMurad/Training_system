from rest_framework import serializers
from .models import Lesson, View


class LessonSerializer(serializers.ModelSerializer):
    viewed = serializers.SerializerMethodField()
    viewed_time = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'url', 'duration', 'viewed', 'viewed_time']

    def get_viewed(self, lesson):
        user = self.context['request'].user
        try:
            view = View.objects.get(user=user, lesson=lesson)
            return view.viewed
        except View.DoesNotExist:
            return False

    def get_viewed_time(self, lesson):
        user = self.context['request'].user
        try:
            view = View.objects.get(user=user, lesson=lesson)
            return view.viewed_time
        except View.DoesNotExist:
            return 0
