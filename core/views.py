from django.shortcuts import render, redirect
from .models import Produto, Cliente
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProdutoForm

def index(request):
    context = {'curso': 'Desenvolvimento de Sistemas'}
    prod = Produto.objects.all()
    context = {'prod': prod}
    return render(request, 'index.html', context)

@login_required(login_url='urlentrar')
def contato(request):
    context = { 
        'nome': 'Sarah',
        'telefone': '(47)91234-5678',
        'email': 'sarah@email.com'
    }
    return render(request, 'contato.html', context)

@login_required(login_url='urlentrar')
def produtos(request):
    prod = Produto.objects.all()
    context = {'prod': prod}
    return render(request, 'produtos.html', context)

@login_required(login_url='urlentrar')
def clientes(request):
    clientes = Cliente.objects.all()
    context = {'cli': clientes}
    return render (request, 'clientes.html', context)

@login_required(login_url='urlentrar')
def cadastraClientes(request):
    return render (request, 'cadastraClientes.html')

@login_required(login_url='urlentrar')
def salvarClientes(request):
    if request.method == 'POST':
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

    return redirect("urlclientes")

@login_required(login_url='urlentrar')
def editaCliente(request, id):
    cliente = Cliente.objects.get(id=id)

    if request.method == "GET":
        context = {'cliente': cliente}
        return render(request, 'editaCliente.html', context)
  
    cliente.nome = request.POST.get('nome')
    cliente.sobrenome = request.POST.get('sobrenome')
    cliente.telefone = request.POST.get('telefone')
    cliente.email = request.POST.get('email')
    cliente.cpf = request.POST.get('cpf')
    cliente.save()
    return redirect('urlclientes')

def entrar(request):
    if request.method == "GET":
        return render(request, "entrar.html")
    
    elif request.method == "POST":
        usuario = request.POST.get("usuario")
        senha = request.POST.get("senha")
        user = authenticate(username=usuario, password=senha)

        if user is not None:
            login(request, user)
            return redirect("urlprodutos")
        else:
            messages.error(request, "Falha na autenticação!")
            return render(request, "entrar.html")

def sair(request):
    logout(request)
    return redirect('urlentrar')
    
def salvarProdutos(request):
    if request.method == 'GET':
        form = ProdutoForm()
        return render(request, 'salvarProdutos.html', {'form': form})
    else:
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('urlprodutos')
        
def editarProdutos(request, id):
    produto = Produto.objects.get(id=id)
    if request.method == 'GET':
        form = ProdutoForm(instance=produto)
        return render(request, 'editarProdutos.html', {'form': form})
    else:
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('urlprodutos')