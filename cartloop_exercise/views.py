from django.http.response import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from .serializers import CreateConversationSerializer, CreateChatSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Client, Schedule, Store, Operator, Conversation, Chat, Discount
import re
from datetime import datetime, timedelta
import pytz


@csrf_exempt
def create_conversation(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CreateConversationSerializer(data=data)
        if serializer.is_valid():
            store = Store.objects.filter(id=data.get('store_id'))[0]
            client = Client.objects.filter(id=data.get('client_id'))[0]
            operator = Operator.objects.filter(id=data.get('operator_id'))[0]
            conversation = Conversation(store=store, client=client, operator=operator)
            conversation.save()
            return JsonResponse(CreateConversationSerializer(conversation).data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'Bad Request': 'This request needs to be a POST one.'}, status=400)

@csrf_exempt
def extract_conversation(request, id):
    if request.method == 'GET':
        all_conversations = Conversation.objects.all()
        if id <= len(all_conversations):
            conversations = Conversation.objects.filter(id=id)
            if len(conversations) > 0:

                data = {
                    "id": conversations[0].id,
                    "store_id": conversations[0].store.id,
                    "operator_id": conversations[0].operator.id,
                    "operator_group": conversations[0].operator.operator_group,
                    "client_id": conversations[0].client.id,
                    "status": conversations[0].status,
                    "chats": list(Chat.objects.filter(conversation=conversations[0]).values())
                }

                return JsonResponse(data, status=200)
        else:
            return JsonResponse({"Error": "ID doesn't exist!"}, status=404)
    else:
        return JsonResponse({'Bad Request': 'This request needs to be a GET one.'}, status=400)

@csrf_exempt
def create_chat(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CreateChatSerializer(data=data)
        if serializer.is_valid():
            conversation = Conversation.objects.filter(id=data.get('conversation_id'))[0]
            discount = Discount.objects.filter(id=data.get('discount_id'))[0]
            payload = re.sub(r'[^aA-zZ1234567890{}$%_\/~@#$%^&\s()!?-]', '', data.get('payload'))
            if len(payload) > 300:
                return JsonResponse({'ERROR': 'Payload is longer than 300 characters!'}, status=400)

            user = Client.objects.filter(id=conversation.client.id)[0].user
            chat= Chat(conversation=conversation, payload=payload, discount=discount, user=user)
            chat.save()

            client_tz = pytz.timezone(Client.objects.filter(id=conversation.client.id)[0].timezone)
            min_limit = client_tz.localize(datetime(chat.created_date.year, chat.created_date.month, chat.created_date.day, 9, 0))
            max_limit = client_tz.localize(datetime(chat.created_date.year, chat.created_date.month, chat.created_date.day, 20, 0))
            chat_date = client_tz.localize(chat.created_date)
            if chat_date > min_limit and chat_date < max_limit:
                schedule_date = chat.created_date
            elif chat_date > max_limit and chat_date <= datetime(chat.created_date.year, chat.created_date.month, chat.created_date.day, 23, 59):
                schedule_date = min_limit.timedelta(days=1).replace(hour=9,minute=0)
            else:
                schedule_date = client_tz.localize(datetime(chat.created_date.year, chat.created_date.month, chat.created_date.day, 9, 0))

            schedule = Schedule(chat=chat, schedule_date=schedule_date)

            schedule.save()
            return JsonResponse(CreateChatSerializer(chat).data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'Bad Request': 'This request needs to be a POST one.'}, status=400)

@csrf_exempt
def extract_chat(request, id):
    if request.method == 'GET':
        all_chats = Chat.objects.all()
        if id <= len(all_chats):
            chats = Chat.objects.filter(id=id)
            if len(chats) > 0:

                data = {
                    "id": chats[0].id,
                    "payload": chats[0].payload,
                    "user_id": Client.objects.filter(user=chats[0].user)[0].id,
                    "conversation_id": chats[0].conversation.id,
                    "created_date": chats[0].created_date,
                    "status": chats[0].status
                }

                return JsonResponse(data, status=200)
        else:
            return JsonResponse({"Error": "ID doesn't exist!"}, status=404)
    else:
        return JsonResponse({'Bad Request': 'This request needs to be a GET one.'}, status=400)
