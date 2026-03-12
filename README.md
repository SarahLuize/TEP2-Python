# TEP2-Python
Tópicos Especiais em Programação II

🚀 Comandos do Projeto

    1️⃣ Migrações (ordem correta)
        # 1º - Criar as migrações
        python manage.py makemigrations

        # 2º - Aplicar as migrações
        python manage.py migrate

    👤 Criar Superusuário
        python manage.py createsuperuser

    ⚡ Rodar o Servidor (porta 8080(usado no IFSC))
        python manage.py runserver 8080

📦 Dependências do Projeto

    ⚡ Instalar django-localflavor
        pip install django-localflavor

        💻 Uso no código:
        from localflavor.br.models import BRCPFField

    ⚡ Instalar tzdata
    python -m pip install tzdata

    ⚡ Instalar Bootstrap5
    -m pip install django-bootstrap-v5

    ⚡ Instalar Pillow
    -m pip install pillow
