from django.shortcuts import render
from .serializers import MessageSerialzer,ConversationSerialzer
from .models import Conversation,Message
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.


class CreateConversationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        conversation = Conversation.objects.create(user=request.user)
        return Response({
            "message": "Conversation created successfully",
            "conversation_id": conversation.id
        })
    

class ListConversationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        conversations = Conversation.objects.filter(user=request.user).order_by("-created_at")
        serializer = ConversationSerialzer(conversations,many=True)
        return Response(serializer.data)
    
class GetConversationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        try:
            conversation = Conversation.objects.get(id=id,user=request.user)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=404)
        
        serializer = ConversationSerialzer(conversation)
        return Response(serializer.data)
