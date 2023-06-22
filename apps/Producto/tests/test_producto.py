import pytest
from rest_framework import status
from django.test.client import encode_multipart
from .fixtures import crear_productos, api_client, get_default_test_user, crear_producto
# from apps.producto.tests.fixtures import api_client, get_default_test_user
from ..models import detalleorden, producto, orden



@pytest.mark.django_db
def test_api_usuario_logueado(api_client, get_default_test_user):
    client = api_client
    client.force_authenticate(user = get_default_test_user)
    response = client.get('/producto/', logging=get_default_test_user)
    assert response.status_code == status.HTTP_200_OK



"""6. Verificar que al ejecutar el endpoint de modificación del stock de
 un producto, actualiza correctamente dicho stock."""

@pytest.mark.django_db
def test_api_modificacion_producto(api_client, crear_producto):
     client = api_client
     client.force_authenticate(user=get_default_test_user)
     producto1 = crear_producto
     #producto_refresco = crear_producto
     data = {
         'stock': 15
     }

     edicion = client.patch(f'/producto/{producto1.id}/', data, format='json')
     
     print(producto1.id)
     print(edicion)
     
     producto_refresco = producto.objects.get(id=producto1.id)
     producto_refresco.refresh_from_db()
     assert producto_refresco.stock == (producto1.stock + 5)




