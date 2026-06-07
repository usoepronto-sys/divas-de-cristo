from django.contrib import admin
from .models import Categoria, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'ordem', 'ativa')
    list_editable = ('ordem', 'ativa')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'categoria',
        'preco',
        'tamanho',
        'disponivel',
        'destaque',
        'ordem',
        'criado_em',
    )

    list_editable = (
        'preco',
        'disponivel',
        'destaque',
        'ordem',
    )

    list_filter = (
        'categoria',
        'disponivel',
        'destaque',
        'criado_em',
    )

    search_fields = (
        'nome',
        'descricao',
        'tamanho',
    )

    list_per_page = 20