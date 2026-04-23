from django.shortcuts import render, redirect
from .models import Produto, Cliente, Avaliacao
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProdutoForm
import io
import urllib, base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
        thisnome = request.POST.get('nome')
        thissobrenome = request.POST.get('sobrenome')
        thisemail = request.POST.get('email')
        thistelefone = request.POST.get('telefone')
        thiscpf = request.POST.get('cpf')
        cliente = Cliente(
            nome = thisnome,
            sobrenome = thissobrenome,
            email = thisemail,
            telefone = thistelefone,
            cpf = thiscpf
        )
        cliente.save()
        return redirect("urlclientes")
    
    return render(request, "salvarClientes.html")

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

@login_required(login_url='urlentrar')
def apagaCliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
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
        
def get_dataframe():
    # Busca todos os dados do banco e retorna um DataFrame do Pandas
    avaliacoes = Avaliacao.objects.all().values()
    df = pd.DataFrame(list(avaliacoes))
    return df

def plot_to_base64(fig):
    # Converte uma figura Matplotlib para uma string base64 para ser usada no HTML
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return urllib.parse.quote(string)

def distribuicao_das_notas_view(df):
    plt.figure(figsize=(10, 6))
    df['review_score'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Distribuição das Notas das Avaliações')
    plt.xlabel('Nota Score')
    plt.ylabel('Quantidade de Avaliações')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    grafico_distribuicao_notas = plot_to_base64(plt.gcf())
    plt.close()

    return grafico_distribuicao_notas

def livros_mais_avaliados_view(request):
    top_10_livros = df['title'].value_counts().nlargest(10)
    plt.figure(figsize=(12, 8))
    top_10_livros.sort_values().plot(kind='barh', color='coral')
    plt.title('Top 10 Livros com Mais Avaliações')
    plt.xlabel('Número de Avaliações')
    plt.ylabel('Título do Livro')
    plt.tight_layout()
    grafico_top_livros = plot_to_base64(plt.gcf())
    plt.close()
    
    context = {
        'grafico_top_livros': grafico_top_livros,
        'total_avaliacoes': len(df)
    }
    
    return render(request, 'core/livros_mais_avaliados_view', context)

def usuarios_mais_ativos_view(df):
    usuarios_mais_ativos = df['profile_name'].value_counts().dropna().nlargest(15)
    plt.figure(figsize=(12, 6))
    plt.barh(usuarios_mais_ativos, width=usuarios_mais_ativos)
    plt.title('Top 15 Usuários Mais Ativos')
    plt.xlabel('Número de Avaliações')
    plt.ylabel('Usuário')
    plt.tight_layout()
    
    grafico_usuarios_ativos =  plot_to_base64(plt.gcf())
    plt.close()
    
    return grafico_usuarios_ativos

def evolucao_reviews_view(df): 
    df['ano'] = pd.to_datetime(df['review_time'], unit='s').dt.year
    qtdeAvalpAno = df.groupby('ano').size()

    plt.figure(figsize=(12, 6))
    plt.plot(qtdeAvalpAno.index, qtdeAvalpAno.values, marker='o')
    plt.title('Evolução do Número de Avaliações por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de Avaliações')
    
    grafico_evolucao_reviews =  plot_to_base64(plt.gcf())
    plt.close()

    return grafico_evolucao_reviews

def preco_vs_score_view(df):
    grafico_preco_score = df[df['price'] > 0]
    filtrar = df.sample(n=300)

    plt.figure(figsize=(12,8))
    plt.scatter(df['price'], df['review_score'], alpha=0.3)
    plt.xlabel('Preço')
    plt.ylabel('Avaliação - Pontuação')
    plt.title('Correlação entre Preço e Nota da Avaliação')
    
    grafico_preco_score = plot_to_base64(plt.gcf())
    plt.close()
    
    return grafico_preco_score

def sentimento_reviews_view(df):   

    def classificarSentimento(texto):
        avlPos = ['good', 'great', 'excellent', 'I loved', 'I recommend', 'amazing', 'enchanted', 'fun', 'awesome', 'must-read', 'must read', 'fantastic', 'interesting', 'brilliant', 'greatest triology', 'greatest', 'the best', 'excelente', 'lovely book', 'best books ever', 'astonishing', 'great novel', 'fabulous']
        avlNeg = ['bad','terrible', 'disappointing', 'disappointed', "I didn't like it", 'terrible', 'weakest', 'sin profundidad', 'awful', 'out ot date', 'useless']

        texto = str(texto).lower()
        if any(p in texto for p in avlPos): return 'Positivo'
        if any(p in texto for p in avlNeg): return 'Negativo'   
        return 'Neutro'

    df['sentimento'] = df['review_summary'].fillna('').apply(classificarSentimento)
    contagem = df['sentimento'].value_counts()
        
    plt.figure(figsize=(12,8))
    plt.pie(contagem, autopct='%1.1f%%')
    plt.title('Distribuição de Sentimentos nos Sumários das Avaliações')
    plt.tight_layout()
    grafico_sentimento_reviews = plot_to_base64(plt.gcf())
    plt.close()

    return grafico_sentimento_reviews

def dashboard(request):
    df = get_dataframe()
    grafico_preco_score = preco_vs_score_view(df)
    grafico_distribuicao_das_notas = distribuicao_das_notas_view(df)
    grafico_evolucao_reviews = evolucao_reviews_view(df)
    grafico_sentimento_reviews = sentimento_reviews_view(df)
    grafico_usuarios_ativos = usuarios_mais_ativos_view(df)
    context = {
        # Ordem dos gráficos
        # 1. distribuicao_das_notas_view
        # 2. livros_mais_avaliados_view
        # 3. usuarios_mais_ativos_view
        # 4. evolucao_reviews_view
        # 5. preco_vs_score_view
        # 6 sentimento_reviews_view
        'grafico_distribuicao_das_notas': grafico_distribuicao_das_notas,
        #adicionar 2
        'grafico_usuarios_ativos': grafico_usuarios_ativos,
        'grafico_evolucao_reviews': grafico_evolucao_reviews,
        'grafico_preco_score': grafico_preco_score,
        'grafico_sentimento_reviews' : grafico_sentimento_reviews,
    }
    return render(request, 'dashboard.html', context)