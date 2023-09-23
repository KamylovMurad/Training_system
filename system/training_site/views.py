from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LessonSerializer
from .models import Access, Lesson


class AllLessonView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_products = Access.objects.filter(user=user, access=True).values_list('product', flat=True)
        lessons = Lesson.objects.filter(product__id__in=accessible_products)
        return lessons




