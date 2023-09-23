from django.db import models
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import AllLessonSerializer, ProductSerializer, ProductStatsSerializer
from .models import Access, Lesson, Product, View


class AllLessonView(ListAPIView):
    """
    View for listing all accessible lessons for a user.

    This view returns a list of lessons that a user has access to.

    Attributes:
        serializer_class (serializers.Serializer): The serializer class for serializing the lesson data.
        permission_classes (list): The list of permission classes that restrict access to authenticated users.

    Methods:
        get_queryset(self): Get the queryset of lessons accessible to the authenticated user.
    """
    serializer_class = AllLessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset of lessons accessible to the authenticated user.

        Returns:
            queryset: A queryset of lessons that the user has access to.
        """
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
    """
    View for listing lessons for a specific product.

    This view returns a list of lessons for a specified product that the user has access to.

    Attributes:
        serializer_class (serializers.Serializer): The serializer class for serializing the lesson data.
        permission_classes (list): The list of permission classes that restrict access to authenticated users.

    Methods:
        get_queryset(self): Get the queryset of lessons for the specified product accessible to the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Get the queryset of lessons for the specified product accessible to the authenticated user.

        Returns:
            queryset: A queryset of lessons for the specified product that the user has access to.
        """
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
    """
    View for retrieving statistics about products.

    This view returns statistics about each product on the platform, including total views, total duration,
    total students, and acquisition percentage.

    Attributes:
        serializer_class (serializers.Serializer): The serializer class for serializing the product statistics.

    Methods:
        get_queryset(self): Get the queryset of product statistics.
    """
    serializer_class = ProductStatsSerializer

    def get_queryset(self):
        """
        Get the queryset of product statistics.

        Returns:
            queryset: A queryset of product statistics.
        """
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
