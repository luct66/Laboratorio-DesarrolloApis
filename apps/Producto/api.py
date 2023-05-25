from rest_framework import viewsets
from apps.Producto.models import detalleorden, orden, producto
from .serializers import DetalleOrdenSerializer, OrdenSerializer, ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = producto.objects.all()
    serializer_class = ProductoSerializer

    
class OrdenViewSet(viewsets.ModelViewSet):
    queryset = orden.objects.all()
    serializer_class = OrdenSerializer
    
    
    def perform_destroy(self, orden):
        # Recorro los datos del detalle y devuelvo el producto al stock
        for detalle in orden.detalles_orden.all():
            producto_orden = detalle.producto
            producto_orden.stock = producto_orden.stock + detalle.cantidad
            producto_orden.save()
        # Finalmente Elimino la orden
        orden.delete()


class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = detalleorden.objects.all()
    serializer_class = DetalleOrdenSerializer
    













    