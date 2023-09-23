from django.db import models
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import AllLessonSerializer, ProductSerializer, ProductStatsSerializer
from .models import Access, Lesson, Product, View


class AllLessonView(ListAPIView):
    serializer_class = AllLessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_products = Access.objects.filter(
            user=user,
            access=True
        ).values_list(
            'product',
            flat=True
        )
        lessons = Lesson.objects.filter(product__id__in=accessible_products)
        return lessons


class ProductLessonView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        product = self.kwargs['product_name']
        product = get_object_or_404(Product, name=product)
        access = Access.objects.filter(
            user=user,
            product=product,
            access=True
        ).exists()
        if not access:
            return Lesson.objects.none()
        lessons = Lesson.objects.filter(product=product)
        return lessons


class ProductStatsView(ListAPIView):
    serializer_class = ProductStatsSerializer

    def get_queryset(self):
        products = Product.objects.all()
        stats = []

        for product in products:
            total_views = View.objects.filter(lesson__product=product).count()
            total_duration = View.objects.filter(
                lesson__product=product
            ).aggregate(
                total_duration=models.Sum('viewed_time')
            )[
                'total_duration'
            ]
            total_students = Access.objects.filter(product=product, access=True).count()
            total_users = Access.objects.filter(product=product).count()
            acquisition_percentage = (total_students / total_users) * 100 if total_users > 0 else 0

            stats.append({
                'product_id': product.id,
                'product_name': product.name,
                'total_views': total_views,
                'total_duration': total_duration,
                'total_students': total_students,
                'acquisition_percentage': acquisition_percentage,
            })

        return stats
