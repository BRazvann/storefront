from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import include, url

urlpatterns = [
    path('conversations/', views.create_conversation),
    path('conversations/<int:id>/', views.extract_conversation),
    path('chats/', views.create_chat),
    path('chats/<int:id>/', views.extract_chat)
    
]
