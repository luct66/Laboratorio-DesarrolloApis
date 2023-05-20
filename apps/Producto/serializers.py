from rest_framework import serializers
from .models import producto,detalleorden,orden

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = producto
        fields = '__all__'

    def validate_stock(self, value):
        if value == 0:
            raise serializers.ValidationError('El Stock tiene que ser mayor que cero.')
        return value



class DetalleOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = detalleorden
        fields = ['id','producto', 'cantidad']

    def obtener_id(self, detalleOrden):
        return detalleOrden.obtenerID()

class OrdenSerializer(serializers.ModelSerializer):
    detalles_orden = DetalleOrdenSerializer(many=True)
    total_orden = serializers.SerializerMethodField(method_name='obtener_total_orden')

    class Meta:
        model= orden
        fields = ['id',
                  'fecha_hora', 'detalles_orden', 'total_orden']


    def obtener_total_orden(self, orden):
        return orden.get_total()

