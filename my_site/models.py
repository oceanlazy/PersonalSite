from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=25)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
