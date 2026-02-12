from django.urls import path
from .views import index, contato

urlpatterns = [
    path('', index, name="urlindex"),
    path('contato', contato, name="urlcontato"),
]
