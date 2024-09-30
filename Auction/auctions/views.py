from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": auction_listing.objects.all()
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

def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image"]
        category = request.POST["category"]
        new_listing = auction_listing(title = title, description = description, starting_bid = starting_bid, image = image, category = category, user_id = request.user.id, active = True, winning_id = 0)
        new_listing.save()
        return HttpResponseRedirect(reverse("create_listing"))
    return render(request, "auctions/listing.html", {
        "categories": Categories.objects.all()
    })

def view_listing(request, id):
    listing = auction_listing.objects.get(id=id)
    if listing.active:
        winningUser = None
    else:
        try:
            winningUser = User.objects.get(id = listing.winning_id)
        except:
            winningUser = None
    try:
        watchlisted = watchlist.objects.get(user_id = request.user.id, listing_id = listing.id)
        watchlisted = True
    except:
        watchlisted = False

    if request.user.id == listing.user_id:
        owner = True
    else:
        owner = False
    
    if request.method == "POST":
        if not listing.active:
            if 'new_comment' in request.POST:
                messages.error(request, 'The listing is closed.', extra_tags='comment-error')
            else:
                messages.error(request, 'The listing is closed.', extra_tags='listing-error')
            return render(request, "auctions/view.html", {
                "listing": listing,
                "comments": auction_comment.objects.filter(listing_id = listing.id),
                "watchlisted": watchlisted,
                "active": listing.active,
                "owner": owner,
                "winning_user": winningUser
            })
        
        if not request.user.is_authenticated:
            if 'new_comment' in request.POST:
                messages.error(request, 'Sign-in required.', extra_tags='comment-error')
            else:
                messages.error(request, 'Sign-in required.', extra_tags='listing-error')
            return render(request, "auctions/view.html", {
                "listing": listing,
                "comments": auction_comment.objects.filter(listing_id = listing.id),
                "watchlisted": watchlisted,
                "active": listing.active,
                "owner": owner
            })  

        if 'new_bid' in request.POST:
            try:
                bid = float(request.POST['new_bid'])
                if isinstance(bid, float):
                    if listing.starting_bid < bid:
                        listing.starting_bid = bid
                        listing.winning_id = request.user.id
                        listing.save()
                        try:
                            new_bid = auction_bid.objects.get(listing_id = listing.id, user_id= request.user.id)
                            new_bid.bid = bid
                        except:
                            new_bid = auction_bid(bid = bid, listing_id = listing.id, user_id = request.user.id)
                        new_bid.save()
                        messages.success(request, 'Your bid was successful', extra_tags='listing-success')
                        return render(request, "auctions/view.html", {
                            "listing": listing,
                            "comments": auction_comment.objects.filter(listing_id = listing.id),
                            "watchlisted": watchlisted,
                            "active": listing.active,
                            "owner": owner
                        })
                    else:
                        messages.error(request, 'Bid must be higher than the current price.', extra_tags='listing-error')
            except:
                messages.error(request, 'Please enter a valid bid.', extra_tags='listing-error')
        elif 'new_comment' in request.POST:
            comment_content = request.POST['new_comment']
            if comment_content != "":
                new_comment = auction_comment(title = request.user.username, content = comment_content, user_id = request.user.id, listing_id = listing.id)
                new_comment.save()
        elif 'close' in request.POST:
            listing.active = False
            listing.save()
            messages.success(request, 'Listing Closed.', extra_tags='listing-success')
            try:
                winningUser = User.objects.get(id = listing.winning_id)
            except:
                winningUser = None
        elif request.POST['watchlist'] == 'watchlist':
            if watchlisted:
                watchlistCheck = watchlist.objects.get(user_id = request.user.id, listing_id = listing.id)
                watchlistCheck.delete()
                messages.success(request, 'Item removed from your watchlist', extra_tags='listing-success')
                watchlisted = False
            else:
                addToWatchlist = watchlist(user_id = request.user.id, listing_id = listing.id)
                addToWatchlist.save()
                messages.success(request, 'Item added to your watchlist.', extra_tags='listing-success')
                watchlisted = True
    return render(request, "auctions/view.html", {
        "listing": listing,
        "comments": auction_comment.objects.filter(listing_id = listing.id),
        "watchlisted": watchlisted,
        "active": listing.active,
        "owner": owner,
        "winning_user": winningUser
    })

@login_required(login_url='/login')
def watchlists(request):
    listings = auction_listing.objects.all()
    listing_ids = []
    for objects in listings:
        listing_ids.append(objects.id)
    try:
        watchlistCheck = watchlist.objects.filter(user_id = request.user.id, listing_id__in = listing_ids)
        watchlistIds = []
        for entry in watchlistCheck:
            watchlistIds.append(entry.listing_id)
    except:
        watchlistIds = []

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "watchlist_ids": watchlistIds
    })

def category(request):
    category = request.GET.get('category')

    return render(request, "auctions/category.html", {
        "category": category,
        "listings": auction_listing.objects.all()
    })