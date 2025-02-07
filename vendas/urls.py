from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    path('', views.lista_vendas, name='lista_vendas'),
    path('nova/', views.nova_venda, name='nova_venda'),
    path('<int:pk>/', views.detalhe_venda, name='detalhe_venda'),
    path('<int:pk>/editar/', views.editar_venda, name='editar_venda'),
    path('<int:pk>/excluir/', views.excluir_venda, name='excluir_venda'),
]

