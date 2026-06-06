from django.shortcuts import render
from .models import Produto


def home(request):

    produtos_destaque = Produto.objects.filter(
        destaque=True,
        disponivel=True
    )

    produtos = Produto.objects.filter(
        disponivel=True
    )

    contexto = {
        'produtos_destaque': produtos_destaque,
        'produtos': produtos
    }

    return render(request, 'home.html', contexto)