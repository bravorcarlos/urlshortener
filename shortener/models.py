from django.db import models
from django.contrib.auth.models import User
from hashids import Hashids

# Create your models here.
class Link(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField(max_length=200)
    code = models.TextField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    clicks = models.PositiveIntegerField(default=0)
    last_click = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:
            self.code = Hashids(min_length=8).encode(self.pk)
            self.save()