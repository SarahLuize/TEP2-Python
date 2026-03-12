from django.urls import path
from .views import index, contato, produtos, clientes, salvarClientes, editaCliente, entrar, sair
from .views import  salvarProdutos, editarProdutos
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name="urlindex"),
    path('contato', contato, name="urlcontato"),
    path('produtos', produtos, name="urlprodutos"),
    path('clientes', clientes, name="urlclientes"),
    path('salvarClientes', salvarClientes, name="urlsalvarClientes"),
    path('editaCliente/<int:id>', editaCliente, name="urleditaCliente"),
    path('entrar', entrar, name="urlentrar"),
    path('sair', sair, name="urlsair"),
    path('salvarProdutos', salvarProdutos, name="urlsalvarProdutos"),
    path('editarProdutos/<int:id>', editarProdutos, name='urleditarProdutos'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)