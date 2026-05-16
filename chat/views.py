from django.shortcuts import render
from .serializers import MessageSerialzer,ConversationSerialzer,PdfUploadSerialzer
from .models import Conversation,Message,PdfDocument
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rag.chroma import search_chunk
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
    
# class ConversationDetailView(APIView):
#     permission_classes = [IsAuthenticated]
    


#     def get(self,request,id):
#         try:
#             conversation = Conversation.objects.get(id=id,user=request.user)
#         except Conversation.DoesNotExist:
#             return Response({"error": "Conversation not found"}, status=404)
        
#         serializer = ConversationSerialzer(conversation)
#         return Response(serializer.data)
    

    
class ConversationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,id,user):
        try:
            return Conversation.objects.get(id=id,user=user)
        except Conversation.DoesNotExist:
            return None
        
    def get(self,request,id):

        conversation = self.get_object(id,request.user)

        if not conversation:
            return Response(
                {"error":"conversation not found"},status=404
            )
        
        serializer = ConversationSerialzer(conversation)

        return Response (serializer.data)
    def delete(self,request,id):

        conversation = self.get_object(id,request.user)
        if not conversation:
            return Response(
                {"error":"conversation not found"},status=404
            )
        
        conversation.delete()

        return Response({
            "message":
            "conversation deleted sucessfully"
        })
                
class ConversationMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        try :
            conversation = Conversation.objects.get(id=id,user=request.user)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=404)

        messages = Message.objects.filter(
            conversation=conversation
        ).order_by("timestamp")

        serializer = MessageSerialzer(messages, many=True)

        return Response(serializer.data)

    



class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        user_message = request.data.get("message")
        pdf_id = request.data.get("pdf_id")

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
               
         # CHAT HISTORY

        chat_history = ""
        for msg in messages:
            chat_history  += f"{msg.sender}:{msg.content}\n"

        #RAG Context 
        pdf = None 

        
        context = ''

        if pdf:

            chunks = search_chunk(pdf.id,user_message)
            context = "\n\n".join(chunks)

            prompt = f"""
You are a helpful AI assistant.

CHAT HISTORY:
{chat_history}

PDF CONTEXT:
{context}

USER QUESTION:
{user_message}

Rules:
- Answer naturally
- Use PDF context if relevant
- If answer is not in PDF, answer normally
"""



        ai_response = generate_ai_response(prompt)


        ai_message = Message.objects.create(
            conversation=conversation,
            sender="ai",
            content=ai_response
        )




        

        return Response({
            "user_message": user_message,
            "ai_response": ai_message.content
        })


class PDFUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PdfUploadSerialzer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)