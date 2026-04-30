from django.urls import path
from .views import ListConversationView,CreateConversationView


urlpatterns = [
    path("conversations/create/",CreateConversationView.as_view(),name="create-conversation"),
    path("conversations/",ListConversationView.as_view(),name="list-conversations")

]