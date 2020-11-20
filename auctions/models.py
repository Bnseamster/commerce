from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass
    

class Auction_listing(models.Model):
    createdBy= models.ForeignKey(User, on_delete=models.CASCADE)
    category= models.CharField(max_length=64)
    name= models.CharField(max_length=64)
    date_posted = models.DateTimeField(auto_now_add=True)
    description= models.TextField(max_length=500, blank=True, default='None Provided')
    picture= models.CharField(max_length= 200, blank=True)
    start_date= models.DateField()
    end_date= models.DateField()
    closed= models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Bid(models.Model):
    bid= models.IntegerField()
    listing= models.ManyToManyField(Auction_listing, blank=True, related_name='bids')
    bidder= models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name='prevbids')
    
    def __str__(self):
        return str(self.bid)

class Listing_comments(models.Model):
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=256)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')

    def __str__(self):
        return self.text

class Watchlist(models.Model):
    listing = models.ManyToManyField(Auction_listing, blank=True, related_name='onwatchlist')
    user= models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='watchlist')

    def __str__(self):
        return str(self.listing)