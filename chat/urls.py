from django.urls import path
from .views import ListConversationView,CreateConversationView,SendMessageView,ConversationDetailView,ConversationMessagesView,PDFUploadView


urlpatterns = [
    path("conversations/create/",CreateConversationView.as_view(),name="create-conversation"),
    path("conversations/",ListConversationView.as_view(),name="list-conversations"),
    path("conversations/<int:id>/", ConversationDetailView.as_view()),
    # path("conversation/<int:id>",),
    path("conversations/<int:id>/messages/",ConversationMessagesView.as_view()),
    path("message/",SendMessageView.as_view()),
    path("upload/", PDFUploadView.as_view()),
]