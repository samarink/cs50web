from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category


def index(request):
    return redirect('listings')


def listing(request, id):
    lst = Listing.objects.get(pk=id)
    return render(request, 'auctions/listing.html', {
        'listing': lst,
        'comments': Comment.objects.filter(listing=lst),
        'bids': lst.bids.order_by('-amount'),
        'in_watchlist': lst in request.user.watchlist.all()
    })


def listings(request):
    return render(request, 'auctions/listings.html', {
        'listings': Listing.objects.filter(active=True),
    })


def new_listing(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        try:
            category, _ = Category.objects.get_or_create(
                name=request.POST['category'])

            new_listing = Listing(
                title=request.POST['title'],
                description=request.POST['description'],
                price=request.POST['price'],
                img_url=request.POST['img_url'],
                user=request.user,
                category=category
            )
            new_listing.save()

            return redirect('listing', id=new_listing.id)
        except IntegrityError:
            return HttpResponse('could not save that')

    else:
        return render(request, 'auctions/new_listing.html')


def listing_close(request, id):
    listing = Listing.objects.get(pk=id)

    highest_bid = listing.bids.order_by('-amount').first()
    listing.winner = highest_bid.user
    listing.active = False
    listing.save()
    return redirect('listing', id=id)


def new_comment(request):
    if request.method == 'POST':
        new_comm = Comment(
            body=request.POST['body'],
            user=request.user,
            listing=Listing.objects.get(pk=request.POST['listing_id'])
        )
        new_comm.save()
        return redirect('listing', request.POST['listing_id'])


def new_bid(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        listing = Listing.objects.get(pk=request.POST['listing_id'])

        if listing.highest_bid < amount:
            listing.highest_bid = amount
            listing.save()

            bid = Bid(amount=amount, listing=listing, user=request.user)
            bid.save()
            return redirect('listing', id=listing.id)
        else:
            return HttpResponse('invalid amount')


def watchlist(request):
    return render(request, 'auctions/listings.html', {
        'listings': request.user.watchlist.all()
    })


def new_watchlist(request):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=request.POST['listing_id'])
        user = User.objects.get(pk=request.user.id)
        user.watchlist.add(listing)
        user.save()
        return redirect('listing', listing.id)


def remove_watchlist(request):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=request.POST['listing_id'])
        user = User.objects.get(pk=request.user.id)
        user.watchlist.remove(listing)
        user.save()
        return redirect('listing', listing.id)


def list_category(request, name):
    category = Category.objects.get(name=name)
    return render(request, 'auctions/listings.html', {
        'listings': Listing.objects.filter(category=category)
    })


def all_categories(request):
    return render(request, 'auctions/all_categories.html', {
        'categories': Category.objects.all()
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
