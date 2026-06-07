from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('colecao/<slug:slug>/', views.produtos_por_categoria, name='produtos_por_categoria'),
    path('produto/<int:id>/', views.detalhe_produto, name='detalhe_produto'),
]