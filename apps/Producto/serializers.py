import requests
from rest_framework import serializers
from .models import producto,detalleorden,orden
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = producto
        fields = ['nombre','precio', 'stock']

    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError('El Stock tiene que ser mayor que cero.')
        return value


class DetalleOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = detalleorden
        fields = ['orden','producto', 'cantidad']

    def validate(self,atributos):
        productos = atributos['producto']
        cantidad = atributos['cantidad']

    # Valida si el stock es suficiente
        if cantidad > productos.stock:
            raise serializers.ValidationError("No hay suficiente stock en el producto")
        return atributos

    def create(self,data):
        ordennew = data['orden']
        productonew = data['producto']
        cantidadnew = data['cantidad']

        productonew.stock = productonew.stock - cantidadnew    
        productonew.save()
        existe = detalleorden.objects.filter(producto=productonew.id).exists()
        if not existe:
            detalle_orden = detalleorden.objects.create(orden=ordennew,producto=productonew,cantidad=cantidadnew)
            detalle_orden.save()
            return detalle_orden
        else:
            raise serializers.ValidationError("Este producto ya se agrego a la orden")

class OrdenSerializer(serializers.ModelSerializer): 
    detalles_orden = DetalleOrdenSerializer(many=True).allow_null
    total_orden = serializers.SerializerMethodField(method_name='get_total')
    total_orden_usd = serializers.SerializerMethodField(method_name='get_total_usd')
    
    class Meta:
        model= orden
        fields = ['fecha_hora', 'detalles_orden',
                   'total_orden', 'total_orden_usd']
        """
        fields = ['id','fecha_hora']
        """
    def get_total(self, orden):
        return orden.get_total_orden()


    def get_total_usd(self, orden):
        json = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales').json()
        dolar_blue_compra = json[1]['casa']['venta'].replace(',', '.')
        cotizar_dolar = float(orden.get_total_orden()) / float(dolar_blue_compra)
        return str(round(cotizar_dolar, 2)) + ' USD'
