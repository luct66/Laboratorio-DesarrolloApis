from uuid import uuid4
from django.db import models
from django.utils.timezone import datetime

# Create your models here.

class producto(models.Model):
    #uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    nombre = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        texto = "Nombre: {0} - Precio: {1} - Cantidad: {2}"
        return texto.format(self.nombre,self.precio,self.stock)
    

class orden(models.Model):
    #uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    fecha_hora = models.DateTimeField(default=datetime.today)
    def __str__(self):
        texto = "Fecha y Hora - {0}"
        return texto.format(self.fecha_hora)

    def get_total_orden(self):
        total_orden = 0
        for detalle in self.detalles_orden.all():
            total_orden = total_orden + detalle.get_total_detalle()
        return total_orden

class detalleorden(models.Model):
    #uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    orden = models.ForeignKey(orden,on_delete=models.CASCADE, related_name='detalles_orden')
    cantidad = models.DecimalField(max_digits=8,decimal_places=2)
    producto = models.ForeignKey(producto,on_delete=models.CASCADE)   
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self):
        texto = "Orden: {0} - Cantidad: {1} - Producto: {2} - Precio_unitario: {3}"
        return texto.format(self.orden,self.cantidad,self.producto,self.precio_unitario,)
    
    def save(self, *args, **kwargs):
        self.precio_unitario = self.producto.__getattribute__('precio')
        super(detalleorden, self).save(*args, **kwargs)

    def get_total_detalle(self):
        precio_total_detalle = self.precio_unitario * self.cantidad
        return precio_total_detalle
    






    
    """
    def __str__(self):
        return self.nombre

    def __float__(self):
        return self.stock
    """