from rest_framework import serializers
from .models import Conversation, Chat

class CreateConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'store_id', 'operator_id', 'client_id']

class CreateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'conversation_id', 'payload', 'discount_id']