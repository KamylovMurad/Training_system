from rest_framework import serializers
from .models import Lesson, View, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class AllLessonSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    viewed = serializers.SerializerMethodField()
    viewed_time = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'url', 'duration', 'viewed', 'viewed_time', 'product']

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


class ProductSerializer(serializers.ModelSerializer):
    viewed = serializers.SerializerMethodField()
    viewed_time = serializers.SerializerMethodField()
    last_viewed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'url', 'duration', 'viewed', 'viewed_time', 'last_viewed']

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

    def get_last_viewed(self, lesson):
        user = self.context['request'].user
        try:
            view = View.objects.get(user=user, lesson=lesson)
            return view.last_viewed_date
        except View.DoesNotExist:
            return


class ProductStatsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    total_views = serializers.IntegerField()
    total_duration = serializers.IntegerField()
    total_students = serializers.IntegerField()
    acquisition_percentage = serializers.FloatField()
