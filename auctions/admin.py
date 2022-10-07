from django.contrib import admin

from .models import (Watchlist, Listing, Bid, Comment, Category)

admin.site.register(Watchlist)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)