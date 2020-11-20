from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count

from .models import User, Auction_listing, Listing_comments, Bid, Watchlist
import datetime



listings = []

def index(request):
    allListings = Auction_listing.objects.all()
    for listing in allListings:
        delta = listing.end_date - datetime.date.today()
    
    
        if (delta.days < 0):
            listing.closed = True
            listing.save()
    
    return render(request, "auctions/index.html",{
        "listings":Auction_listing.objects.filter(closed=False)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing_page(request, listing_id):
    if request.method == 'POST':
        if request.POST.get('button') == 'bid':
            get_bid(listing_id, request)
        
        elif request.POST.get('button') == 'comment':
            add_comment(listing_id, request)

    
    listing= Auction_listing.objects.filter(id=listing_id).first()
    
    topBid = listing.bids.aggregate(Max('bid'))
    Bids = Bid.objects.filter(bid=topBid['bid__max']).first()
    bidCount = listing.bids.aggregate(Count('bid'))
    topBidder = Bids.bidder
    
    comments = listing.comments.all()
    
    delta = listing.end_date - datetime.date.today()
    
    
    if ( (close_listing(request.POST.get('close')) == True) or (delta.days < 0) ):
        close = True
        listing.closed = close
        listing.save()
    else:
        close = False



    return render(request, "auctions/listing_page.html", {
            'listing': listing,
            'bids': topBid,
            'bidCount': bidCount,
            'comments': comments,
            'showClose': show_close(listing_id, request),
            'close': close,
            'topBidder': topBidder,
            'currentUser': request.user,
            'daysTillEnd': delta.days
    })

def active_listings(request):
    
    return render(request, "auctions/category.html",{
    "listings":Auction_listing.objects.all()
    })

def all_categories(request):
    categories = ["Electronics", "Clothing", "Food", "Sports", "Home", "Books", "Musical Instruments"]
    return render(request, "auctions/all_categories.html",{
        "categories": categories
    })
    
def display_category(request, category):
     #query models for all listings with this specific category

    
    return render(request, "auctions/category.html",{
        "category":str(category),
        "listings":Auction_listing.objects.filter(category=f"{category}")
    })

@login_required
def addToWatchlist(request, listing_id):
    listing = Auction_listing.objects.get(id=listing_id)

    
    try:
        userWatchlist = Watchlist.objects.get(user=request.user) #get list of user's watched items from models
           
    except:
        userWatchlist = Watchlist(user=request.user)
        userWatchlist.save()
    
    userWatchlist.listing.add(Auction_listing.objects.get(id=listing_id))
    
    watchlist = userWatchlist.listing.all()
    

    return render(request, "auctions/watchlist.html",{
        "watchlist":watchlist
    })

@login_required
def show_watchlist(request):

    try:
        userWatchlist = Watchlist.objects.get(user=request.user) #get list of user's watched items from models
           
    except:
        userWatchlist = Watchlist(user=request.user)
        userWatchlist.save()
    
    
    
    watchlist = userWatchlist.listing.all()
    print(watchlist.count())
    
    if watchlist.count() != 0:
        return render(request, "auctions/watchlist.html",{
            "watchlist":watchlist
        })
    else:
        return render(request, "auctions/watchlist.html",{
            "watchlist":[]
        })

@login_required
def create_listing(request):
    if request.method== 'GET':
        return render(request, "auctions/create_listing.html",{

    })
    elif request.method == 'POST':

        sd = request.POST['start-date'].split('-')
        sd = [int(x) for x in sd]
        startDate = datetime.date(sd[0], sd[1], sd[2])
        ed=  request.POST['end-date'].split('-')
        ed = [int(x) for x in ed]
        endDate= datetime.date(ed[0], ed[1], ed[2])

        listing = Auction_listing(createdBy= request.user, category= request.POST['category'], name= request.POST['listingName'].capitalize(), description= request.POST['description'], picture= request.POST['listingPic'], start_date= startDate, end_date= endDate)
        listing.save()
        bid = Bid(bid= request.POST['startingBid'])
        bid.save()
        bid.listing.add(listing)
        
        
        return render(request, "auctions/index.html",{
        "listings":Auction_listing.objects.filter(closed=False)
    })

def get_bid(listing_id,request):
    listing = Auction_listing.objects.get(id=listing_id)
    listing.save()
    bid = Bid(bid= request.POST['newBid'], bidder= request.user)
    bid.save()
    bid.listing.add(listing)
    
    
    


def add_comment(listing_id,request):
    listing = Auction_listing.objects.get(id=listing_id)        
    
    comments = Listing_comments(text= request.POST['newComment'], listing=listing)
    comments.save()

def show_close(listing_id, request):
    listing = Auction_listing.objects.get(id=listing_id)
    user = request.user

    if listing.createdBy == user:
        return True
    else:
        return False

def close_listing(response):
    if response == 'close':
        return True
    else:
        return False