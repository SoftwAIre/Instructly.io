from django.contrib import admin

# Register your models here.
from .models import User, Bid, Category, Comment, Listing

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Listing)
