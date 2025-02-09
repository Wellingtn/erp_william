from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('estoque/', include('estoque.urls')),
    path('vendas/', include('vendas.urls')),
    path('vendedoras/', include('vendedoras.urls')),
    path('clientes/', include('clientes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

