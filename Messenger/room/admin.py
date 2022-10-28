from django.contrib import admin
from .models import Room, ChatUser, Message

admin.site.register(Room)
admin.site.register(ChatUser)
admin.site.register(Message)
