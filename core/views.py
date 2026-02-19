from django.shortcuts import render
from .models import Produto, Cliente

def index(request):
    context = {'curso': 'Desenvolvimento de Sistemas'}
    return render(request, 'index.html', context)

def contato(request):
    context = { 
        'nome': 'Sarah',
        'telefone': '(47)91234-5678',
        'email': 'sarah@email.com'
    }
    return render(request, 'contato.html', context)

def produtos(request):
    prod = Produto.objects.all()
    context = {'prod': prod}
    return render(request, 'produtos.html', context)

def clientes(request):
    clientes = Cliente.objects.all()
    context = {'cli': clientes}
    return render (request, 'clientes.html', context)