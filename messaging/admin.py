from django.contrib import admin
from .models import Messenger, Message, MessageLog

admin.site.register(Messenger)
admin.site.register(Message)
admin.site.register(MessageLog)
