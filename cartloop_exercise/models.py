from django.db import models
import pytz

ALL_TZS = sorted((tz, tz) for tz in pytz.all_timezones)

class Store(models.Model):
    name = models.CharField(max_length=25, unique=True)
    timezone = models.CharField(choices=ALL_TZS, max_length=64)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Discount(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=False)
    discount_code = models.CharField(max_length=15)

    def __str__(self):
        return self.discount_code

class Operator(models.Model):
    user = models.CharField(max_length=25, unique=True)
    operator_group = models.CharField(max_length=25)

    def __str__(self):
        return self.user

class Client(models.Model):
    user = models.CharField(max_length=25, unique=True)
    timezone = models.CharField(choices=ALL_TZS, max_length=64)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user

class Conversation(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=15, default="Unresolved")

class Chat(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=False)
    payload = models.TextField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=False)
    user = models.CharField(max_length=25)
    created_date = models.DateTimeField(null=False, auto_now_add=True)
    status = models.CharField(max_length=15, default="NEW")

class Schedule(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False)
    schedule_date = models.DateTimeField(null=False)

    def __str__(self):
        return self.chat