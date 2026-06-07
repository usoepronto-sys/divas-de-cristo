from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    ordem = models.PositiveIntegerField(default=0)
    ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    nome = models.CharField(max_length=150)
    descricao = models.TextField()

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    tamanho = models.CharField(
        max_length=50,
        blank=True
    )

    imagem = models.ImageField(
        upload_to='produtos/'
    )

    disponivel = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    ordem = models.PositiveIntegerField(default=0)

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['ordem', '-criado_em']

    def __str__(self):
        return self.nome


class FotoProduto(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='fotos'
    )

    imagem = models.ImageField(
        upload_to='produtos/galeria/'
    )

    ordem = models.PositiveIntegerField(default=0)

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Foto do Produto'
        verbose_name_plural = 'Fotos do Produto'
        ordering = ['ordem', '-criado_em']

    def __str__(self):
        return f'{self.produto.nome} - Foto {self.id}'


class Reserva(models.Model):
    STATUS_NOVO = 'novo'
    STATUS_ATENDIMENTO = 'atendimento'
    STATUS_RESERVADO = 'reservado'
    STATUS_VENDIDO = 'vendido'
    STATUS_CANCELADO = 'cancelado'

    STATUS_CHOICES = [
        (STATUS_NOVO, 'Novo'),
        (STATUS_ATENDIMENTO, 'Em atendimento'),
        (STATUS_RESERVADO, 'Reservado'),
        (STATUS_VENDIDO, 'Vendido'),
        (STATUS_CANCELADO, 'Cancelado'),
    ]

    cliente = models.CharField(max_length=150)
    whatsapp = models.CharField(max_length=30)

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='reservas'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOVO
    )

    observacao = models.TextField(
        blank=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.cliente} - {self.produto.nome}'