from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Cria grupos de acesso: Gerente e Vendedor"

    def handle(self, *args, **kwargs):
        gerente, _ = Group.objects.get_or_create(name="Gerente")
        vendedor, _ = Group.objects.get_or_create(name="Vendedor")

        gerente.permissions.clear()
        vendedor.permissions.clear()

        gerente_perms = Permission.objects.filter(
            content_type__app_label__in=["loja", "auth"]
        )

        vendedor_perms = Permission.objects.filter(
            content_type__app_label="loja",
            codename__in=[
                "add_produto",
                "change_produto",
                "view_produto",
                "add_categoria",
                "change_categoria",
                "view_categoria",
            ]
        )

        gerente.permissions.set(gerente_perms)
        vendedor.permissions.set(vendedor_perms)

        self.stdout.write(self.style.SUCCESS("Grupos Gerente e Vendedor criados com sucesso."))