from django.urls import path
from .views import index, contato, produtos, clientes, cadastraClientes, salvarClientes, editaCliente

urlpatterns = [
    path('', index, name="urlindex"),
    path('contato', contato, name="urlcontato"),
    path('produtos', produtos, name="urlprodutos"),
    path('clientes', clientes, name="urlclientes"),
    #path('cadastraClientes', cadastraClientes, name="urlcadastraClientes"),
    path('salvarClientes', salvarClientes, name="urlsalvarClientes"),
    path('editaCliente/<int:id>', editaCliente, name="urleditaCliente")
]
