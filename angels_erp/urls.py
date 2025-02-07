from django.contrib import admin
from django.urls import path, include
from core.views import logout_view

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('estoque/', include('estoque.urls')),
    path('vendas/', include('vendas.urls')),
    path('vendedoras/', include('vendedoras.urls')),
    path('clientes/', include('clientes.urls')),
    path('logout/', logout_view, name='logout'),
]

