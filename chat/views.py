from django.shortcuts import render
from .serializers import MessageSerialzer,ConversationSerialzer
from .models import Conversation,Message
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.
from ai.gemini import generate_ai_response

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




class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        user_message = request.data.get("message")

        if not conversation_id or not user_message:
            return Response({"error": "conversation_id and message are required"}, status=400)

        try:
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=404)

        Message.objects.create(
            conversation=conversation,
            sender="user",
            content=user_message
        )
        messages = Message.objects.filter(
            conversation = conversation,
        ).order_by("timestamp")
        
        chat_history = ""
        for msg in messages:
            chat_history  += f"{msg.sender}:{msg.content}\n"

        
        ai_response = generate_ai_response(chat_history)


        ai_message = Message.objects.create(
            conversation=conversation,
            sender="ai",
            content=ai_response
        )




        

        return Response({
            "user_message": user_message,
            "ai_response": ai_message.content
        })