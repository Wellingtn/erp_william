from django.urls import path
from . import views

app_name = 'vendedoras'

urlpatterns = [
    path('', views.lista_vendedoras, name='lista_vendedoras'),
    path('adicionar/', views.adicionar_vendedora, name='adicionar_vendedora'),
    path('<int:pk>/editar/', views.editar_vendedora, name='editar_vendedora'),
    path('<int:pk>/', views.detalhe_vendedora, name='detalhe_vendedora'),
    path('<int:pk>/acerto/', views.realizar_acerto, name='realizar_acerto'),
    path('<int:pk>/adicionar-estoque/', views.adicionar_estoque_vendedora, name='adicionar_estoque_vendedora'),
]

