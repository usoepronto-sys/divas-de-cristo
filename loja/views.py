from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Produto, Categoria


def home(request):
    busca = request.GET.get('busca', '').strip()

    categorias = Categoria.objects.all()

    produtos_destaque = Produto.objects.filter(
        destaque=True,
        disponivel=True
    ).order_by('-criado_em')[:4]

    produtos = Produto.objects.filter(
        disponivel=True
    ).order_by('-criado_em')

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) |
            Q(descricao__icontains=busca) |
            Q(tamanho__icontains=busca) |
            Q(categoria__nome__icontains=busca)
        )

    paginator = Paginator(produtos, 4)
    pagina_numero = request.GET.get('page')
    produtos_paginados = paginator.get_page(pagina_numero)

    contexto = {
        'categorias': categorias,
        'produtos_destaque': produtos_destaque,
        'produtos': produtos_paginados,
        'busca': busca,
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

    produtos_relacionados = Produto.objects.filter(
        categoria=produto.categoria,
        disponivel=True
    ).exclude(
        id=produto.id
    ).order_by('-criado_em')[:4]

    contexto = {
        'produto': produto,
        'produtos_relacionados': produtos_relacionados,
    }

    return render(request, 'produto.html', contexto)