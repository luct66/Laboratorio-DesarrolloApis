import requests
from rest_framework import serializers
from .models import producto,detalleorden,orden
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = producto
        fields = ['id','nombre','precio', 'stock']

    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError('El Stock tiene que ser mayor que cero.')
        return value

class DetalleOrdenSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.SerializerMethodField()
    class Meta:
        model = detalleorden
        fields = ['id','orden','producto','producto_nombre', 'cantidad']

    def get_producto_nombre(self, detalle_orden):
        return detalle_orden.producto.nombre
    
    def validate(self,atributos):
        productos = atributos['producto']
        cantidad = atributos['cantidad']
        if cantidad > productos.stock:
            raise serializers.ValidationError("No hay suficiente stock en el producto")
        return atributos

    def create(self,data):
        ordennew = data['orden']
        productonew = data['producto']
        cantidadnew = data['cantidad']
        existe = detalleorden.objects.filter(producto=productonew.id).exists()
        if not existe:
            productonew.stock = productonew.stock - cantidadnew    
            productonew.save()
            detalle_orden = detalleorden.objects.create(orden=ordennew,producto=productonew,cantidad=cantidadnew)
            detalle_orden.save()
            return detalle_orden
        else:
            raise serializers.ValidationError("Este producto ya se agrego a la orden")

class OrdenSerializer(serializers.ModelSerializer): 
    detalles_orden = DetalleOrdenSerializer(read_only=True,many=True)
    total_orden = serializers.SerializerMethodField(method_name='get_total')
    total_orden_usd = serializers.SerializerMethodField(method_name='get_total_usd')
    class Meta:
        model= orden
        fields = ['id','fecha_hora', 'detalles_orden','total_orden', 'total_orden_usd']
    
    def get_total(self, orden):
        return orden.get_total_orden()

    def get_total_usd(self, orden):
        json = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales').json()
        dolar_blue_compra = json[1]['casa']['venta'].replace(',', '.')
        cotizar_dolar = float(orden.get_total_orden()) / float(dolar_blue_compra)
        return str(round(cotizar_dolar, 2)) + ' USD'
