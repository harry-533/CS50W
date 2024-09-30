from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(auction_listing)
admin.site.register(Categories)
admin.site.register(auction_bid)
admin.site.register(auction_comment)
admin.site.register(watchlist)