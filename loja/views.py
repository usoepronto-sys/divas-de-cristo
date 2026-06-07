from django.shortcuts import render, get_object_or_404
from .models import Produto, Categoria


def home(request):
    categorias = Categoria.objects.filter(ativa=True)

    produtos_destaque = Produto.objects.filter(
        destaque=True,
        disponivel=True
    ).order_by('ordem', '-criado_em')

    produtos = Produto.objects.filter(
        disponivel=True
    ).order_by('ordem', '-criado_em')

    contexto = {
        'categorias': categorias,
        'produtos_destaque': produtos_destaque,
        'produtos': produtos,
    }

    return render(request, 'home.html', contexto)


def produtos_por_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug, ativa=True)

    produtos = Produto.objects.filter(
        categoria=categoria,
        disponivel=True
    ).order_by('ordem', '-criado_em')

    contexto = {
        'categoria': categoria,
        'produtos': produtos,
    }

    return render(request, 'categoria.html', contexto)