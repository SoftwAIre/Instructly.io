import json
import decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import IntegrityError
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django import forms

from .models import Bid, Category, Comment, Listing, User


# class CreateListingForm(ModelForm):
#     class Meta:
#         model = Listing
#         fields = ['category', 'title', 'goal', 'description', 'due_date', 'image_url', 'starting_bid', 'tutoring_time']
        
#     def __init__(self, *args, **kwargs):
#         super(CreateListingForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs["class"] = "form-control"


class CreateListingForm(forms.Form):
    category = forms.CharField(max_length=25)
    # title = forms.CharField(max_length=25)
    # goal = forms.CharField(max_length=255)
    # description = forms.TextField(blank=True)
    # image_url = forms.URLField(blank=True)
    # seller = forms.ForeignKey("User", on_delete=forms.CASCADE, related_name="listings")
    # starting_bid = forms.DecimalField(max_digits=19, decimal_places=2)
    # bid_winner = forms.ForeignKey("User", on_delete = forms.CASCADE, blank=True, null=True, related_name="listing_won")
    due_date = forms.DateField()
    # tutoring_time = forms.DecimalField(default=1, max_digits=2, decimal_places=1)
    # session_completed = forms.BooleanField(default=False)



@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        amount = decimal.Decimal(request.POST["bid"])
        pitch = request.POST["pitch"]

        # Ensure bid is valid.
        if listing.seller == request.user:
            return render(request, "auctions/error.html", {
                "message": "Could not place bid: you cannot bid on your own items."
            })
        # elif listing.bids.count() == 0 and amount < listing.starting_bid:
        #     return render(request, "auctions/error.html", {
        #         "message": "Could not place bid: bid must be at least starting bid."
        #     })
        # elif listing.bids.count() > 0 and amount <= listing.price():
        #     return render(request, "auctions/error.html", {
        #         "message": "Could not place bid: bid must be greater than current bid."
        #     })
        bid = Bid(amount=amount, pitch=pitch, bidder=request.user, listing=listing)
        bid.save()
    # elif request.method == "GET":
    #     listing = get_object_or_404(Listing, pk=listing_id)
    #     if listing.seller == request.user:
    #         bids = Bid.objects.filter(listing=listing)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.order_by("name").all()
    })


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(active=True, category=category).order_by("-creation_time").all()
    return render(request, "auctions/index.html", {
        "title": f"Active Listings in {category.name}: {listings.count()}",
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
        winner_id = request.POST["bid_winner"]
        winner = get_object_or_404(User, pk=int(winner_id))
        listing.bid_winner = winner
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
    listings = Listing.objects.filter(active=True).order_by("due_date").all()
    listings_count = listings.count()
    return render(request, "auctions/index.html", {
        "title": f"Active Listings Available: {listings_count}",
        "listing_counts": listings_count,
        "listings": listings
    })


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    on_watchlist = request.user.is_authenticated and (listing in request.user.watchlist.all())
    if listing.seller.id == request.user.id or request.user.is_anonymous:
        my_bids = []
    else:
        my_bids = listing.bids.filter(bidder=request.user)
    return render(request, "auctions/listing.html", {
        "comments": listing.comments.order_by("-creation_time").all(),
        "listing": listing,
        "my_bids": my_bids,
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
    won_listings = Listing.objects.filter(bid_winner=profile_user).order_by("due_date").all()

    return render(request, "auctions/profile.html", {
        "is_me": request.user.id == user_id,
        "title": f"{profile_user.username}'s Profile",
        "profile_user": profile_user,
        "profile": profile_user.tutor_profile,
        "credentials": profile_user.linkedin_url,
        "listings": won_listings
    })


@login_required
def edit_profile(request, user_id):
    """send edit profile to database"""
    # variable name may not be optimal here.
    try:
        profile_user = User.objects.get(pk=int(user_id))
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if int(profile_user.id) != int(request.user.id):
        return JsonResponse({
            "error": "invalid profile edit."
        }, status=400)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("profile") is not None:
            profile_user.tutor_profile = data["profile"]
            profile_user.save()
            return JsonResponse({
                "profile": profile_user.tutor_profile
            })
        elif data.get("tagline") is not None:
            profile_user.tagline = data["tagline"]
            profile_user.save()
            return JsonResponse({
                "tagline": profile_user.tagline
            })
        else: 
            return JsonResponse({
                "error": "PUT request failed."
            }, status=400)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


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
def listings_won(request):
    listings = Listing.objects.filter(bid_winner=request.user).order_by('due_date').all()
    return render(request, "auctions/index.html", {
        "title": "Listings Won",
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

