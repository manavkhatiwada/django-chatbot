from django.urls import path
from .views import ListConversationView,CreateConversationView,GetConversationView,SendMessageView


urlpatterns = [
    path("conversations/create/",CreateConversationView.as_view(),name="create-conversation"),
    path("conversations/",ListConversationView.as_view(),name="list-conversations"),
    path("conversation/<int:id>/", GetConversationView.as_view()),
    # path("conversation/<int:id>",),
    path("message/",SendMessageView.as_view()),
    

]