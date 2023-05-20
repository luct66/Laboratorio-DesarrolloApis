from django.contrib import admin

from apps.Producto.models import detalleorden, orden, producto

# Register your models here.

admin.site.register(producto)

admin.site.register(orden)

admin.site.register(detalleorden)

