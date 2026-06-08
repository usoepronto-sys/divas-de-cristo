from django.contrib.auth.apps import AuthConfig


class CustomAuthConfig(AuthConfig):
    verbose_name = "Cadastro de Usuários"