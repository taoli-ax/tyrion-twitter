from django.contrib import admin
from friendships.models import Friendship
# Register your models here.


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('from_user','to_user','created_at')