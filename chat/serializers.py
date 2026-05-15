from rest_framework import serializers
from .models import Conversation, Message,PdfDocument


class MessageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','sender','conversation','content','timestamp']

class ConversationSerialzer(serializers.ModelSerializer):
    messages = MessageSerialzer(many=True,read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id','created_at','title','messages']

class PdfUploadSerialzer(serializers.ModelSerializer):
    class Meta:
        model = PdfDocument
        fields = ["id","file"]