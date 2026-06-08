from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Categoria, Produto, FotoProduto, Reserva


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'ordem', 'ativa')
    list_editable = ('ordem', 'ativa')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)
    list_per_page = 20


class FotoProdutoInline(admin.TabularInline):
    model = FotoProduto
    extra = 3
    fields = ('preview', 'imagem', 'ordem')
    readonly_fields = ('preview',)
    ordering = ('ordem', '-criado_em')

    def preview(self, obj):
        if obj and obj.imagem:
            return format_html(
                '<a href="{0}" target="_blank">'
                '<img src="{0}" style="width:80px;height:100px;object-fit:cover;border-radius:8px;border:1px solid #ddd;" />'
                '</a>',
                obj.imagem.url
            )
        return 'Sem imagem'

    preview.short_description = 'Prévia'


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'preview_lista',
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

    readonly_fields = ('preview_grande',)
    list_per_page = 20
    inlines = [FotoProdutoInline]

    fieldsets = (
        ('Informações principais', {
            'fields': (
                'preview_grande',
                'categoria',
                'nome',
                'descricao',
                'preco',
                'tamanho',
                'imagem',
            )
        }),

        ('Controle da vitrine', {
            'fields': (
                'disponivel',
                'destaque',
                'ordem',
            )
        }),
    )

    def preview_lista(self, obj):
        if obj and obj.imagem:
            return format_html(
                '<a href="{0}" target="_blank">'
                '<img src="{0}" style="width:60px;height:80px;object-fit:cover;border-radius:8px;border:1px solid #ddd;" />'
                '</a>',
                obj.imagem.url
            )
        return 'Sem imagem'

    preview_lista.short_description = 'Foto'

    def preview_grande(self, obj):
        if obj and obj.imagem:
            return format_html(
                '''
                <a href="{0}" target="_blank">
                    <img src="{0}"
                         style="
                            width:220px;
                            max-width:100%;
                            border-radius:12px;
                            border:1px solid #ddd;
                            box-shadow:0 3px 10px rgba(0,0,0,.15);
                         ">
                </a>
                ''',
                obj.imagem.url
            )

        return format_html(
            '''
            <div style="
                width:220px;
                height:280px;
                border:2px dashed #ccc;
                border-radius:12px;
                display:flex;
                align-items:center;
                justify-content:center;
                color:#888;
            ">
                Sem imagem
            </div>
            '''
        )

    preview_grande.short_description = 'Prévia da imagem principal'


@admin.register(FotoProduto)
class FotoProdutoAdmin(admin.ModelAdmin):
    list_display = ('preview', 'produto', 'ordem', 'criado_em')
    list_filter = ('produto', 'criado_em')
    search_fields = ('produto__nome',)
    readonly_fields = ('preview',)
    list_per_page = 20

    def preview(self, obj):
        if obj and obj.imagem:
            return format_html(
                '<a href="{0}" target="_blank">'
                '<img src="{0}" style="width:80px;height:100px;object-fit:cover;border-radius:8px;border:1px solid #ddd;" />'
                '</a>',
                obj.imagem.url
            )
        return 'Sem imagem'

    preview.short_description = 'Prévia'


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'whatsapp',
        'produto',
        'status_formatado',
        'criado_em',
        'atualizado_em',
    )

    list_filter = (
        'status',
        'produto__categoria',
        'criado_em',
        'atualizado_em',
    )

    search_fields = (
        'cliente',
        'whatsapp',
        'produto__nome',
        'observacao',
    )

    list_editable = (
        'whatsapp',
    )

    readonly_fields = (
        'criado_em',
        'atualizado_em',
    )

    list_per_page = 20

    fieldsets = (
        ('Dados da cliente', {
            'fields': (
                'cliente',
                'whatsapp',
            )
        }),

        ('Produto e atendimento', {
            'fields': (
                'produto',
                'status',
                'observacao',
            )
        }),

        ('Datas', {
            'classes': ('collapse',),
            'fields': (
                'criado_em',
                'atualizado_em',
            )
        }),
    )

    actions = (
        'marcar_em_atendimento',
        'marcar_reservado',
        'marcar_vendido',
        'marcar_cancelado',
    )

    def status_formatado(self, obj):
        cores = {
            Reserva.STATUS_NOVO: '#38bdf8',
            Reserva.STATUS_ATENDIMENTO: '#facc15',
            Reserva.STATUS_RESERVADO: '#a78bfa',
            Reserva.STATUS_VENDIDO: '#22c55e',
            Reserva.STATUS_CANCELADO: '#ef4444',
        }

        cor = cores.get(obj.status, '#ffffff')

        return format_html(
            '<strong style="color:{};">{}</strong>',
            cor,
            obj.get_status_display()
        )

    status_formatado.short_description = 'Status'

    @admin.action(description='Marcar como Em atendimento')
    def marcar_em_atendimento(self, request, queryset):
        queryset.update(status=Reserva.STATUS_ATENDIMENTO)

    @admin.action(description='Marcar como Reservado')
    def marcar_reservado(self, request, queryset):
        queryset.update(status=Reserva.STATUS_RESERVADO)

    @admin.action(description='Marcar como Vendido')
    def marcar_vendido(self, request, queryset):
        queryset.update(status=Reserva.STATUS_VENDIDO)

    @admin.action(description='Marcar como Cancelado')
    def marcar_cancelado(self, request, queryset):
        queryset.update(status=Reserva.STATUS_CANCELADO)


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


admin.site.index_template = 'admin/dashboard.html'

admin.site.site_header = 'Divas de Cristo'
admin.site.site_title = 'Divas de Cristo Admin'
admin.site.index_title = 'Painel Administrativo'


original_index = admin.site.index


def dashboard_index(request, extra_context=None):
    extra_context = extra_context or {}

    extra_context['total_produtos'] = Produto.objects.count()
    extra_context['produtos_disponiveis'] = Produto.objects.filter(disponivel=True).count()
    extra_context['produtos_indisponiveis'] = Produto.objects.filter(disponivel=False).count()
    extra_context['produtos_destaque'] = Produto.objects.filter(destaque=True, disponivel=True).count()
    extra_context['total_categorias'] = Categoria.objects.count()
    extra_context['total_reservas'] = Reserva.objects.count()
    extra_context['reservas_novas'] = Reserva.objects.filter(status=Reserva.STATUS_NOVO).count()
    extra_context['reservas_em_atendimento'] = Reserva.objects.filter(status=Reserva.STATUS_ATENDIMENTO).count()
    extra_context['reservas_vendidas'] = Reserva.objects.filter(status=Reserva.STATUS_VENDIDO).count()
    extra_context['ultimos_produtos'] = Produto.objects.select_related('categoria').order_by('-criado_em')[:5]
    extra_context['ultimas_reservas'] = Reserva.objects.select_related('produto').order_by('-criado_em')[:5]

    return original_index(request, extra_context)


admin.site.index = dashboard_index