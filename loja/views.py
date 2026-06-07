from django.shortcuts import render, get_object_or_404
from .models import Produto, Categoria


def home(request):
    categorias = Categoria.objects.all()

    produtos_destaque = Produto.objects.filter(
        destaque=True,
        disponivel=True
    ).order_by('-criado_em')

    produtos = Produto.objects.filter(
        disponivel=True
    ).order_by('-criado_em')

    contexto = {
        'categorias': categorias,
        'produtos_destaque': produtos_destaque,
        'produtos': produtos,
    }

    return render(request, 'home.html', contexto)


def produtos_por_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)

    produtos = Produto.objects.filter(
        categoria=categoria,
        disponivel=True
    ).order_by('-criado_em')

    contexto = {
        'categoria': categoria,
        'produtos': produtos,
    }

    return render(request, 'categoria.html', contexto)


def detalhe_produto(request, id):
    produto = get_object_or_404(
        Produto,
        id=id,
        disponivel=True
    )

    contexto = {
        'produto': produto,
    }

    return render(request, 'produto.html', contexto)