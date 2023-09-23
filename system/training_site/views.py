from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LessonSerializer
from .models import Access, Lesson, Product


class AllLessonView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_products = Access.objects.filter(user=user, access=True).values_list('product', flat=True)
        lessons = Lesson.objects.filter(product__id__in=accessible_products)
        return lessons


class ProductLessonView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def post(self, request):
        user = self.request.user
        product = request.data.get('product')
        product = get_object_or_404(Product, name=product)
        access = Access.objects.filter(user=user, product=product, access=True).exists()
        if not access:
            return Response(
                {'detail': 'Нет доступа к продукту.'},
                status=status.HTTP_403_FORBIDDEN
            )
        lessons = Lesson.objects.filter(product=product)
        return lessons



