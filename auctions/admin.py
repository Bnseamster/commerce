from django.contrib import admin

from .models import User, Auction_listing, Listing_comments, Bid, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Auction_listing)
admin.site.register(Listing_comments)
admin.site.register(Bid)
admin.site.register(Watchlist)
