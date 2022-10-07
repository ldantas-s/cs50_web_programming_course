from django.contrib.auth.models import AbstractUser
from django.db import models


class Watchlist(models.Model):
    name = models.CharField(max_length=64)
    # user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='watchlist')
    # listing_id = models.ManyToManyField(Listing, related_name='watchlists')

    def __str__(self):
        return self.name

class User(AbstractUser):
    watchlist = models.OneToOneField(Watchlist, on_delete=models.CASCADE, related_name='user')

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    watchlist = models.ManyToManyField(Watchlist, related_name='listing')

    def __str__(self):
        return self.title

class Bid(models.Model):
    value_bid = models.IntegerField()
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')

class Comment(models.Model):
    content = models.CharField(max_length=150)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')

class Category(models.Model):
    name = models.CharField(max_length=64)
    listings = models.ManyToManyField(Listing, related_name='categories')
