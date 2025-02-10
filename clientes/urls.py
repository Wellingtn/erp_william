from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('adicionar/', views.adicionar_cliente, name='adicionar_cliente'),
    path('editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('<int:pk>/', views.detalhe_cliente, name='detalhe_cliente'),
    path('<int:pk>/vendas/', views.vendas_cliente, name='vendas_cliente'),
]
