import json
import decimal

from django import forms
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Bid, Category, Comment, Listing, User


class CreateListingForm(ModelForm):
    """listing form"""
    class Meta:
        """meta class"""
        model = Listing
        fields = [
            'category',
            'title',
            'due_date',
            'goal',
            'description',
            'image_url',
            'starting_bid',
            'tutoring_time'
        ]
        widgets = {
            'due_date': forms.DateInput(
                attrs={'class':'form-control', 'type':'date', 'width': '10px'}),
            "description": forms.Textarea(attrs={'rows':'4'}),
            'tutoring_time': forms.NumberInput(attrs={'step': 0.5}),
            'starting_bid': forms.NumberInput(attrs={'step': 0.5}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


def paginate_helper(request, list_of_posts):
    """this function declutters the pagination request"""
    page = request.GET.get('page', 1)

    paginator = Paginator(list_of_posts, 10)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


@login_required
def bid(request, listing_id):
    """bid on a listing"""
    if request.method == "POST":
        on_listing = get_object_or_404(Listing, pk=listing_id)
        amount = decimal.Decimal(request.POST["bid"])
        pitch = request.POST["pitch"]

        # Ensure bid is valid.
        if on_listing.seller == request.user:
            return render(request, "auctions/error.html", {
                "message": "Could not place bid: you cannot bid on your own items."
            })
        listing_bid = Bid(
            amount=amount,
            pitch=pitch,
            bidder=request.user,
            listing=on_listing)
        listing_bid.save()
    return HttpResponseRedirect(reverse("listing", args=(on_listing.id,)))


# removed categories function that displays all categories
def category(request, category_id):
    """return listings belonging to a category id"""
    this_category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(active=True, category=this_category).order_by("-creation_time").all()
    return render(request, "auctions/index.html", {
        "title": f"Active Listings in {this_category.name}: {listings.count()}",
        "listings": listings,
        "categories": Category.objects.order_by("name").all()
    })


@login_required
def close(request, listing_id):
    """complete the listing"""
    if request.method == "POST":
        this_listing = get_object_or_404(Listing, pk=listing_id)
        if this_listing.seller != request.user:
            return render(request, "auctions/error.html", {
                "message": "You can only close a listing that you own."
            })
        if "bid_winner" in request.POST:
            winner_id = request.POST["bid_winner"]
            winner = get_object_or_404(User, pk=int(winner_id))
            this_listing.bid_winner = winner
        this_listing.active = False
        this_listing.save()
    return HttpResponseRedirect(reverse("listing", args=(this_listing.id,)))


# this is not being used to it's highest potential yet.
# planning to turn this into "reviews" or "referrals"
@login_required
def comment(request, listing_id):
    """return comments"""
    if request.method == "POST":
        content = request.POST["comment"]
        this_listing = get_object_or_404(Listing, pk=listing_id)
        this_comment = Comment(commenter=request.user, content=content, listing=this_listing)
        this_comment.save()
        return HttpResponseRedirect(reverse("listing", args=(this_listing.id,)))
    return JsonResponse({
        "error": "Error occurred with commenting."
    }, status=400)



@login_required
def create(request):
    """create a listing"""
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            create_listing = form.save(commit=False)
            create_listing.seller = request.user
            create_listing.save()
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/create.html", {
            "form": form,
            "categories": Category.objects.order_by("name").all()
        })
    return render(request, "auctions/create.html", {
        "form": CreateListingForm(),
        "categories": Category.objects.order_by("name").all(),
    })


# haven't included functionality for filtering category yet
def index(request, filter_category=None):
    """return listings on landing page"""
    if filter_category:
        listings = Listing.objects.filter(active=True, category=filter_category).order_by("due_date").all()
    else:
        listings = Listing.objects.filter(active=True).order_by("due_date").all()
    listings_count = listings.count()
    return render(request, "auctions/index.html", {
        "title": f"All Active Listings: {listings_count}",
        "listing_counts": listings_count,
        "listings": paginate_helper(request, listings),
        "categories": Category.objects.order_by("name").all()
    })


def listing(request, listing_id):
    """show user listing"""
    this_listing = get_object_or_404(Listing, pk=listing_id)
    on_watchlist = request.user.is_authenticated and (this_listing in request.user.watchlist.all())
    if this_listing.seller.id == request.user.id or request.user.is_anonymous:
        my_bids = []
    else:
        my_bids = this_listing.bids.filter(bidder=request.user)
    return render(request, "auctions/listing.html", {
        "comments": this_listing.comments.order_by("-creation_time").all(),
        "listing": this_listing,
        "my_bids": my_bids,
        "on_watchlist": on_watchlist,
        "categories": Category.objects.order_by("name").all()
    })


def login_view(request):
    """logging in"""
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/login.html", {
            "message": "Invalid username and/or password."
        })
    return render(request, "auctions/login.html")


def logout_view(request):
    """logging out"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def profile(request, user_id):
    """show user profile"""
    profile_user = get_object_or_404(User, pk=user_id)
    won_listings = Listing.objects.filter(bid_winner=profile_user).order_by("due_date").all()

    return render(request, "auctions/profile.html", {
        "is_me": request.user.id == user_id,
        "title": f"{profile_user.username}'s Profile",
        "profile_user": profile_user,
        # change this so that it's just profile, not tutor_profile
        "profile": profile_user.tutor_profile,
        "credentials": profile_user.linkedin_url,
        # did not to paginate here because it's only on one page
        "listings": won_listings,
        "categories": Category.objects.order_by("name").all()
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
        # This needs to be updated so that it's a form that
        # asks for a specific character count. The HTML tags
        # don't do it properly.
        if data.get("tagline") is not None:
            profile_user.tagline = data["tagline"]
            profile_user.save()
            return JsonResponse({
                "tagline": profile_user.tagline
            })
        return JsonResponse({
            "error": "PUT request failed."
        }, status=400)
    return JsonResponse({
        "error": "PUT request required."
    }, status=400)


def tutors(request):
    """return all tutors"""
    all_tutors = User.objects.filter(is_tutor=True)
    return render(request, "auctions/tutors.html", {
        "title": "All Tutors",
        "tutors": paginate_helper(request, all_tutors),
        "categories": Category.objects.order_by("name").all()
    })


def register(request):
    """register for the webpage"""
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
                "message": "Username already taken.",
                "categories": Category.objects.order_by("name").all()
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/register.html")


@login_required
def listings_won(request):
    """return all listings won by current user"""
    listings = Listing.objects.filter(bid_winner=request.user).order_by('due_date').all()
    return render(request, "auctions/index.html", {
        "title": "Listings Won",
        "listings": paginate_helper(request, listings),
        "categories": Category.objects.order_by("name").all()
    })


@login_required
def watchlist(request):
    """Return all listings that are watchlisted by current user"""
    listings = request.user.watchlist.order_by("-creation_time").all()

    return render(request, "auctions/index.html", {
        "title": "My Watchlist",
        "listings": paginate_helper(request, listings),
        "categories": Category.objects.order_by("name").all()
    })


@login_required
def watchlist_add(request):
    """add this_listing to watchlist"""
    if request.method == "POST":
        this_listing = get_object_or_404(Listing, pk=int(request.POST["listing_id"]))
        request.user.watchlist.add(this_listing)
        return HttpResponseRedirect(reverse("listing", args=(this_listing.id,)))
    return render(request, "auctions/error.html", {
        "message": "Could not place bid: you cannot bid on your own items."
    })


@login_required
def watchlist_delete(request):
    """delete this_listing from watchlist"""
    if request.method == "POST":
        this_listing = get_object_or_404(Listing, pk=int(request.POST["listing_id"]))
        request.user.watchlist.remove(this_listing)
        return HttpResponseRedirect(reverse("listing", args=(this_listing.id,)))
    return render(request, "auctions/error.html", {
        "message": "Could not place bid: you cannot bid on your own items."
    })
