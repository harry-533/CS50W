from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followerCount = models.IntegerField(default=0)
    following = models.JSONField(default=list, blank=True)
    imageURL = models.URLField(max_length=256, blank=True, null=True)

class Post(models.Model):
    username = models.CharField(max_length=64)
    user_id = models.IntegerField(default=0)
    body = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    liked_by = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.username}: {self.created_at}"
    

