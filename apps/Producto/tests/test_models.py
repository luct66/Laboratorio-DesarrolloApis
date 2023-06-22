from django.test import TestCase
from ..models import detalleorden, producto, orden

class TestModels(TestCase):

    def setUp(self):
        self.producto1 = producto.objects.create(nombre='Test-Producto1', precio=170, stock=10)
        self.producto2 = producto.objects.create(nombre='Test-Producto2', precio=120, stock=20)
        self.orden1 = orden.objects.create()
        self.detalle1 = detalleorden.objects.create(orden=self.orden1, cantidad=2, producto=self.producto1)
        self.detalle2 = detalleorden.objects.create(orden=self.orden1, cantidad=4, producto=self.producto2)
   
   
























   
    """
    def test_devolver_nombre_producto(self):
        nombre = self.producto1.__str__()
        self.assertEqual(nombre, 'Test-Producto1')

    def test_devolver_stock_producto(self):
        stock = self.producto1.__float__()
        self.assertEqual(stock, 10)

    def test_save_precio_unitario(self):
        precioUnitario = self.detalle1.precio_unitario
        self.assertEqual(precioUnitario, 170)

    def test_get_total_detalle(self):
        precio_total_detalle1 = self.detalle1.get_total_detalle()
        self.assertEqual(precio_total_detalle1, 340)

    def test_get_total_orden(self):
        precio_total_orden1 = self.orden1.get_total_orden()
        self.assertEqual(precio_total_orden1, 820)
        """