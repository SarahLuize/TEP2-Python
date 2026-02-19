from django.shortcuts import render, redirect
from .models import Produto, Cliente
from django.http import HttpResponse

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

def cadastraClientes(request):
    return render (request, 'cadastraClientes.html')

def salvarClientes(request):
    thisNome = request.POST.get('nome')
    thisSobrenome = request.POST.get('sobrenome')
    thisEmail = request.POST.get('email')
    thisTelefone = request.POST.get('telefone')
    thisCPF = request.POST.get('cpf')
    cliente = Cliente(
        nome = thisNome,
        sobrenome = thisSobrenome,
        email = thisEmail,
        telefone = thisTelefone,
        cpf = thisCPF
    )
    cliente.save()

    return redirect('urlclientes')