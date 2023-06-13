from rest_framework import viewsets,status
from apps.Producto.models import detalleorden, orden, producto
from .serializers import DetalleOrdenSerializer, OrdenSerializer, ProductoSerializer
from rest_framework.response import Response


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = producto.objects.all()
    serializer_class = ProductoSerializer
    
    #Esto funciona para path y no para put
    def partial_update(self, request, *args, **kwargs):
        producto = self.get_object()

        # Crear un diccionario con el campo 'stock' y su valor para la actualización
        partial_data = {'stock': request.data.get('stock')}

        # Crear una instancia del serializer solo para actualizar el campo 'stock'
        serializer = self.get_serializer(producto, data=partial_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class OrdenViewSet(viewsets.ModelViewSet):
    queryset = orden.objects.all()
    serializer_class = OrdenSerializer
    
    
    def perform_destroy(self, orden):

        for detalle in orden.detalles_orden.all():
            producto_orden = detalle.producto
            producto_orden.stock = producto_orden.stock + detalle.cantidad
            producto_orden.save()

        orden.delete()


class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = detalleorden.objects.all()
    serializer_class = DetalleOrdenSerializer
    

    def destroy(self,detalle_orden,pk):
        detalle_orden = self.get_object()
        producto_orden = detalle_orden.producto
        producto_orden.stock = producto_orden.stock + detalle_orden.cantidad
        producto_orden.save()
        self.perform_destroy(detalle_orden)
        return Response(status=status.HTTP_204_NO_CONTENT)













    