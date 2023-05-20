from django.db import models

# Create your models here.

class producto(models.Model):
    nombre = models.CharField(max_length=100,blank=False)
    stock = models.IntegerField(blank=False)
    precio = models.FloatField(blank=False)
 
    def __str__(self):
        texto = "{0} - nombre: {1} - stock: {2} - precio: {3}"
        return texto.format(self.nombre, self.stock, self.precio)

class orden(models.Model):
    fecha_hora = models.DateTimeField(auto_now=True)

class detalleorden(models.Model):
    orden = models.ForeignKey(orden,on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=8,decimal_places=2)
    producto = models.ForeignKey(producto,on_delete=models.CASCADE)   
    