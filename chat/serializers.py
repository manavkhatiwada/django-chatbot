from rest_framework import serializers
from .models import Conversation, Message


class MessageSerialzer(serializers.ModelSerializer):
    class meta:
        model = Message
        fields = ['id','sender','conversation','content','timestamp']

class ConversationSerialzer(serializers.ModelSerializer):
    class meta:
        messages = MessageSerialzer(many=True,read_only=True)
        model = Conversation
        fields = ['id','created_at','title','messages']