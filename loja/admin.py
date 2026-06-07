from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Categoria, Produto, FotoProduto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'ordem', 'ativa')
    list_editable = ('ordem', 'ativa')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)


class FotoProdutoInline(admin.TabularInline):
    model = FotoProduto
    extra = 3
    fields = ('imagem', 'ordem')
    ordering = ('ordem', '-criado_em')


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
    inlines = [FotoProdutoInline]


@admin.register(FotoProduto)
class FotoProdutoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'ordem', 'criado_em')
    list_filter = ('produto', 'criado_em')
    search_fields = ('produto__nome',)
    list_per_page = 20


admin.site.unregister(User)


@admin.register(User)
class UsuarioAdmin(UserAdmin):
    list_display = (
        'username',
        'first_name',
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
    )

    fieldsets = (
        ('Dados de acesso', {
            'fields': (
                'username',
                'password',
            )
        }),

        ('Dados pessoais', {
            'fields': (
                'first_name',
                'last_name',
                'email',
            )
        }),

        ('Tipo de acesso', {
            'description': 'Escolha o grupo do usuário: Gerente ou Vendedor. Na maioria dos casos, não mexa nas permissões extras.',
            'fields': (
                'is_active',
                'is_staff',
                'groups',
            )
        }),

        ('Permissões extras avançadas', {
            'classes': ('collapse',),
            'description': 'Use apenas quando quiser liberar permissões específicas além do grupo escolhido.',
            'fields': (
                'user_permissions',
                'is_superuser',
            )
        }),

        ('Datas importantes', {
            'classes': ('collapse',),
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )

    add_fieldsets = (
        ('Criar novo usuário', {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'groups',
            ),
        }),
    )