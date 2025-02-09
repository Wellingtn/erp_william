from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    path('', views.lista_vendas, name='lista_vendas'),
    path('iniciar/', views.iniciar_venda, name='iniciar_venda'),
    path('<int:venda_id>/adicionar-produto/', views.adicionar_produto, name='adicionar_produto'),
    path('<int:venda_id>/finalizar/', views.finalizar_venda, name='finalizar_venda'),
    path('<int:venda_id>/', views.detalhe_venda, name='detalhe_venda'),
    path('<int:venda_id>/carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('<int:venda_id>/finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('api/produto/<int:produto_id>/', views.produto_info, name='produto_info'),
]

