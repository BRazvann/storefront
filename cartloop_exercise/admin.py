from django.contrib import admin
from .models import Store, Operator, Discount, Client, Conversation, Chat, Schedule

admin.site.register(Store)
admin.site.register(Operator)
admin.site.register(Discount)
admin.site.register(Client)
admin.site.register(Conversation)
admin.site.register(Chat)
admin.site.register(Schedule)