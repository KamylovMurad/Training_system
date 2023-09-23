from django.urls import path, include
from .views import AllLessonView

app_name = 'training_site'

urlpatterns = [
    path('all_lessons/', AllLessonView.as_view())
]