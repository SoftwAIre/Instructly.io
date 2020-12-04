from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
# from django.utils.translation import gettext as _


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name="watchers", blank=True)
    wonlist = models.ManyToManyField("Listing", related_name="winners", blank=True)
    specialtylist = models.ManyToManyField("Category", related_name="specialists", blank=True)
    tagline = models.CharField(blank=True, max_length=80)
    tutor_profile = models.TextField(blank=True, max_length=300)
    is_tutor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)
    youtube_channel = models.URLField(blank=True)
    medium_channel = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)


class Category(models.Model):

    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Listing(models.Model):
    active = models.BooleanField(default=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=25)
    goal = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    seller = models.ForeignKey("User", on_delete=models.CASCADE, related_name="sellers")
    starting_bid = models.DecimalField(max_digits=19, decimal_places=2)
    bid_winner = models.ForeignKey("User", on_delete = models.CASCADE, blank=True, null=True, related_name="listing_won")
    due_date = models.DateField(editable=True)
    tutoring_time = models.DecimalField(default=1, max_digits=2, decimal_places=1)
    session_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # def top_bid(self):
    #     try:
    #         return max(self.bids.all(), key=lambda b: b.amount)
    #     except ValueError:
    #         return None

    # def price(self):
    #     bid = self.top_bid()
    #     return bid.amount if bid is not None else self.starting_bid

    # def winner(self):
    #     bid = self.top_bid()
    #     return bid.bidder if bid is not None else None


class Bid(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    bidder = models.ForeignKey("User", on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="bids")
    pitch = models.TextField(blank=True)

    def __str__(self):
        return f"{self.listing} - {self.amount}"


class Comment(models.Model):
    content = models.TextField(blank=True)
    commenter = models.ForeignKey("User", on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.content