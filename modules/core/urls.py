from modules.core.api.v1.view import (
    CredentialView, MessagesListView, MessagesDetailView,
    MessagesDetailTagView)
from django.urls import path


urlpatterns = [
    path('api/v1/credential/', CredentialView.as_view()),
    path('api/v1/message/', MessagesListView.as_view()),
    path('api/v1/message/<int:id>/', MessagesDetailView.as_view()),
    path('api/v1/messages/<str:tag>/', MessagesDetailTagView.as_view()),
]
