from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import (IntegerField)
from django.conf import settings
from datetime import datetime, timedelta, date

from .models import *
import requests

KEY = settings.KEY
URL = settings.URL

class TokensSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True,
        default=serializers.CurrentUserDefault())
    token = serializers.CharField(read_only=True)
    tg_id =serializers.IntegerField()

    class Meta:
        model = Tokens
        fields = []

    def update(self, instance, validated_data):
        instance.tg_id = validated_data.get('tg_id', instance.tg_id)
        instance.save()
        return instance

class MessagesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True,
        default=serializers.CurrentUserDefault())
    message = serializers.CharField()
    date = serializers.DateField(read_only=True)
    name = serializers.CharField(read_only=True, source='user.first_name')
    tg_id = serializers.IntegerField(read_only=True,
        source='user.tokens.tg_id')

    class Meta:
        model = Messages
        fields = []

    def create(self, validated_data):
        post = Messages(
            user = self.context['request'].user,
            message=validated_data['message'],
            date=date.today(),
        )
        post.save()
        user = self.context['request'].user
        msg = validated_data["message"]
        text = f'{user.first_name}, я получил от тебя сообщение:\n{msg}'
        response = requests.post(
            url=f'{URL}{KEY}/sendMessage',
            data={'chat_id': user.tokens.tg_id, 'text': text}
        ).json()
        return post