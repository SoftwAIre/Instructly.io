import decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Bid, Category, Comment, Listing, User


class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image_url', 'category', 'starting_bid']

    def __init__(self, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        amount = decimal.Decimal(request.POST["bid"])

        # Ensure bid is valid.
        if listing.seller == request.user:
            return render(request, "auctions/error.html", {
                "message": "Could not place bid: you cannot bid on your own items."
            })
        elif listing.bids.count() == 0 and amount < listing.starting_bid:
            return render(request, "auctions/error.html", {
                "message": "Could not place bid: bid must be at least starting bid."
            })
        elif listing.bids.count() > 0 and amount <= listing.price():
            return render(request, "auctions/error.html", {
                "message": "Could not place bid: bid must be greater than current bid."
            })
        bid = Bid(amount=amount, bidder=request.user, listing=listing)
        bid.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.order_by("name").all()
    })


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(active=True, category=category).order_by("-creation_time").all()
    return render(request, "auctions/index.html", {
        "title": f"Active Listings in {category.name}",
        "listings": listings
    })


@login_required
def close(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        if listing.seller != request.user:
            return render(request, "auctions/error.html", {
                "message": "You can only close a listing that you own."
            })
        listing.active = False
        listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


@login_required
def comment(request, listing_id):
    if request.method == "POST":
        content = request.POST["comment"]
        listing = get_object_or_404(Listing, pk=listing_id)
        comment = Comment(commenter=request.user, content=content, listing=listing)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create.html", {
            "form": CreateListingForm()
        })


def index(request):
    listings = Listing.objects.filter(active=True).order_by("-creation_time").all()
    return render(request, "auctions/index.html", {
        "title": "Active Listings",
        "listings": listings
    })


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    on_watchlist = request.user.is_authenticated and (listing in request.user.watchlist.all())
    return render(request, "auctions/listing.html", {
        "comments": listing.comments.order_by("-creation_time").all(),
        "listing": listing,
        "on_watchlist": on_watchlist
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


def profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    listings = profile_user.listings.filter(active=True).order_by("-creation_time").all()
    
    return render(request, "auctions/index.html", {
        "is_me": request.user.id == user_id,
        "profile": profile_user.tutor_profile,
        "title": f"{profile_user.username}'s Profile",
        "listings": listings,
        "specialtylist":profile_user.specialtylist
    })


def tutors(request):
    tutors = User.objects.filter(is_tutor=True)
    return render(request, "auctions/tutors.html", {
        "tutors": tutors
    })


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


@login_required
def watchlist(request):
    listings = request.user.watchlist.order_by("-creation_time").all()
    return render(request, "auctions/index.html", {
        "title": "Watchlist",
        "listings": listings
    })

@login_required
def watchlist_add(request):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=int(request.POST["listing_id"]))
        request.user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


@login_required
def watchlist_delete(request):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=int(request.POST["listing_id"]))
        request.user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

