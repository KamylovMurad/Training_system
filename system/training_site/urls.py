from django.urls import path, include
from .views import (
    AllLessonView,
    ProductLessonView
)

app_name = 'training_site'

urlpatterns = [
    path('all_lessons/', AllLessonView.as_view()),
    path('product_lessons', ProductLessonView.as_view())
]