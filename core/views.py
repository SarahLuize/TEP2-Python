from django.shortcuts import render

def index(request):
    context = {'curso': 'Desenvolvimento de Sistemas', 'nome': 'Sarah', 'telefone': '(47)91234-5678', 'email': 'sarah@email.com'}
    return render(request, 'index.html', context)
