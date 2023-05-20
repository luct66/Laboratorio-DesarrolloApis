from rest_framework import viewsets
from apps.Producto.models import detalleorden, orden, producto
from .serializers import DetalleOrdenSerializer, OrdenSerializer, ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = producto.objects.all()
    serializer_class = ProductoSerializer

    
class OrdenViewSet(viewsets.ModelViewSet):
    queryset = orden.objects.all()
    serializer_class = OrdenSerializer

    
class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = detalleorden.objects.all()
    serializer_class = DetalleOrdenSerializer