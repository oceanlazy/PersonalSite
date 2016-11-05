from django.db import models
from django.utils import timezone
from django.contrib import admin


class Publication(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200, default='articles')
    slug = models.SlugField(unique=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class PublicationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
