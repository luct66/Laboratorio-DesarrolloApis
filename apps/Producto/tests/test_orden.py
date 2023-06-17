import pytest
from .fixtures import api_client,crear_productos,crear_orden,get_default_test_user
from django.contrib.auth import get_user_model
from apps.Producto.models import detalleorden
# from apps.producto.models import Producto, Orden, DetalleOrden

@pytest.mark.django_db
def test_api_recuperacion_orden(api_client,crear_orden,crear_productos, get_default_test_user):
    client = api_client
    client.force_authenticate(user=get_default_test_user)
    orden1 = crear_orden
    id_orden1= orden1.id
    cantidad_detalles_orden1= (orden1.detalles_orden).count()
    producto1, producto2 = crear_productos
    ordenes = client.get('/orden/')
    json_data = ordenes.json()
    # Verifico si devuelve la orden correcta
    assert json_data[0]['id'] is not None
    assert json_data[0]['id'] == id_orden1
    # Verifico si devuelve el detalle correcto
    assert detalleorden.objects.filter(orden__id=json_data[0]['id']).count() == cantidad_detalles_orden1
    assert json_data[0]['detalles_orden'][0]['producto'] == producto1.id
    assert json_data[0]['detalles_orden'][1]['producto'] == producto2.id
