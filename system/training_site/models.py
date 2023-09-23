from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Access(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.BooleanField(default=True)


class Lesson(models.Model):
    product = models.ManyToManyField(Product, related_name='lesson')
    name = models.CharField(max_length=50)
    url = models.URLField(default=None)
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    last_viewed_date = models.DateField(auto_now_add=True)
    viewed_time = models.PositiveIntegerField(default=0)
    viewed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        total_duration = self.lesson.duration
        percentage_viewed = (self.viewed_time / total_duration) * 100
        self.viewed = percentage_viewed >= 80
        super(View, self).save(*args, **kwargs)
