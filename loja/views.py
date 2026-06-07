from django.shortcuts import render
from .models import Produto


def home(request):
    produtos_destaque = Produto.objects.filter(
        disponivel=True,
        destaque=True
    ).order_by('ordem', '-criado_em')

    contexto = {
        'produtos_destaque': produtos_destaque,
    }

    return render(request, 'home.html', contexto)