from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class auction_listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.FloatField()
    image = models.URLField(max_length=256, blank=True)
    category = models.CharField(max_length=64, blank=True)
    user_id = models.IntegerField()
    active = models.BooleanField()
    winning_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class auction_bid(models.Model):
    bid = models.FloatField()
    listing_id = models.IntegerField()
    user_id = models.IntegerField()

class auction_comment(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=256)
    user_id = models.IntegerField()
    listing_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class watchlist(models.Model):
    user_id = models.IntegerField()
    listing_id = models.IntegerField()

    
class User(AbstractUser):
    pass
