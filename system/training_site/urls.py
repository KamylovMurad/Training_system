from django.urls import path

from .views import (
    AllLessonView,
    ProductLessonView,
    ProductStatsView
)


app_name = 'training_site'

urlpatterns = [
    path('all_lessons/', AllLessonView.as_view()),
    path('lessons/<str:product_name>/', ProductLessonView.as_view()),
    path('product_stats/', ProductStatsView.as_view())
]
