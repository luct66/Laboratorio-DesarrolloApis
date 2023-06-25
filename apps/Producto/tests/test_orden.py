import pytest
#import self
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .fixtures import orden_data_creada,detalle_data_creada,orden_data,detalle_data,crear_productos,crear_ordenvacia, crear_orden, api_client, get_default_test_user
from ..models import detalleorden, producto, orden
import json
import requests


"""
    1. Verificar que al ejecutar el endpoint de recuperación de una orden,
    se devuelven los datos correctos de la orden y su detalle.
"""

@pytest.mark.django_db
def test_api_recuperacion_orden(api_client,crear_orden,crear_productos, get_default_test_user):
    client = api_client
    client.force_authenticate(user=get_default_test_user)
    orden1 = crear_orden
    id_orden1= orden1.id
    cantidad_detalles_orden1= orden1.detalles_orden.count()
    producto1, producto2 = crear_productos
    ordenes = client.get('/orden/')
    json_data = ordenes.json()
    # Verifico si devuelve la orden correcta
    assert json_data[0]['id'] is not None
    assert json_data[0]['id'] == id_orden1
    # Verifico si devuelve el detalle correcto
    assert detalleorden.objects.filter(orden__id=json_data[0]['id']).count() == cantidad_detalles_orden1
    print(json_data)
    print(producto1.id)
    assert json_data[0]['detalles_orden'][0]['producto'] == producto1.id
    assert json_data[0]['detalles_orden'][1]['producto'] == producto2.id

"""2. Verificar que al ejecutar el endpoint de creación de una orden, ésta
 se cree correctamente junto con su detalle, y que además, se haga actualizado
  el stock de producto relacionado con un detalle de orden. Se debe considerar aquí,
   que los datos de la orden a crear, no posea productos repetidos y que la cantidad
    de productos en el detalle de la orden, sea menor o igual al stock del producto."""

"""3. Verificar que al ejecutar el endpoint de creación de una orden, se produzca 
un fallo al intentar crear una orden cuyo detalle tenga productos repetidos."""


"""4. Verificar que al ejecutar el endpoint de creación de una orden, se
 produzca un fallo al intentar crear una orden donde la cantidad de un producto
  del detalle, sea mayor al stock de ese producto."""


#crear un solo endpoint convocar el contexto que testee por separado cada cosigna como repetidos y cantidad
@pytest.mark.django_db
def test_api_creacion_orden(api_client, get_default_test_user, orden_data_creada,crear_productos, detalle_data_creada):
    client = api_client
    client.force_authenticate(user=get_default_test_user)
    producto1, producto2 = crear_productos
    stock_producto1 = producto1.stock
    stock_producto2 = producto2.stock
    data_orden = {
        'fecha_hora': orden_data_creada['fecha_hora']
    }

    response_orden = client.post('/orden/', data=data_orden)
    assert response_orden.status_code == status.HTTP_201_CREATED

    orden_id = response_orden.json().get('id')

    for detalle in detalle_data_creada:
        detalle['orden'] = orden_id
        response_detalle = client.post('/detalleorden/', data=detalle)
        assert response_detalle.status_code == status.HTTP_201_CREATED

    assert orden.objects.filter(id=orden_id).count() == 1

    response = client.get(f'/orden/{orden_id}/')
    json_data = response.json()

    assert json_data['id'] is not None
    assert json_data['id'] == orden_id

    producto1.refresh_from_db()
    assert producto1.stock == stock_producto1 - json_data['detalles_orden'][0]['cantidad']
    producto2.refresh_from_db()
    assert producto2.stock == stock_producto2 - json_data['detalles_orden'][1]['cantidad']

    assert json_data['detalles_orden'][0]['producto'] == producto1.id
    assert detalleorden.objects.filter(producto=producto1, cantidad=5, orden__id=json_data['id']).count() == 1
    assert json_data['detalles_orden'][1]['producto'] == producto2.id
    assert detalleorden.objects.filter(producto=producto2, cantidad=3, orden__id=json_data['id']).count() == 1

@pytest.mark.django_db
def test_api_creacion_orden_cantidad_stock(api_client, get_default_test_user, orden_data, detalle_data):
    client = api_client
    client.force_authenticate(user=get_default_test_user)

    response_orden = client.post('/orden/', data=orden_data)
    response_detalle1 = client.post('/detalleorden/', data=detalle_data[0])
    response_detalle2 = client.post('/detalleorden/', data=detalle_data[1])
    response_detalle3 = client.post('/detalleorden/', data=detalle_data[2])

    assert response_orden.status_code == status.HTTP_201_CREATED
    assert response_detalle1.status_code == status.HTTP_201_CREATED
    assert response_detalle2.status_code == status.HTTP_201_CREATED
    # Al crear una orden con un detalle con un cantidad mayor al stock no lo permite
    assert response_detalle3.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_api_creacion_orden_repetidos(api_client, get_default_test_user, orden_data, detalle_data):
    client = api_client
    client.force_authenticate(user=get_default_test_user)

    response_orden = client.post('/orden/', data=orden_data)
    response_detalle1 = client.post('/detalleorden/', data=detalle_data[0])
    response_detalle2 = client.post('/detalleorden/', data=detalle_data[1])
    response_detalle3 = client.post('/detalleorden/', data=detalle_data[1])

    assert response_orden.status_code == status.HTTP_201_CREATED
    assert response_detalle1.status_code == status.HTTP_201_CREATED
    assert response_detalle2.status_code == status.HTTP_201_CREATED
    # Al crear una orden con un detalle con un producto repetido  no lo permite
    assert response_detalle3.status_code == status.HTTP_400_BAD_REQUEST


"""5. Verificar que al ejecutar el endpoint de eliminación de una orden, ésta 
se haya eliminado de la base de datos correctamente, junto con su detalle, y que 
además, se haga incrementado el stock de producto relacionado con cada detalle de orden."""

@pytest.mark.django_db
def test_api_eliminacion_orden(api_client,crear_orden,get_default_test_user):
    client = api_client
    client.force_authenticate(user=get_default_test_user)
    orden1 = crear_orden
    id_orden = orden1.id
    detalles = orden1.detalles_orden.all()
    cantidad_detalle1 = detalles[0].cantidad
    cantidad_detalle2 = detalles[1].cantidad
    producto1 = detalles[0].producto
    stock_anterior1 = producto1.stock
    producto2 = detalles[1].producto
    stock_anterior2 = producto2.stock
    # Consulto los elementos de la BD antes de eliminar
    assert orden.objects.filter(id=id_orden).count() == 1
    #assert orden.objects.filter(id=id_orden).count().exists()
    # Planteamos y verificamos el método de eliminación
    orden_eliminada = client.delete("/orden/{}/".format(id_orden))
    assert orden_eliminada.status_code == status.HTTP_204_NO_CONTENT
    # Verificando que que la orden creada se elimino, junto con sus detalles
    assert orden.objects.filter(id=id_orden).count() == 0
    assert detalleorden.objects.filter(orden__id=id_orden).count() == 0
    # Verificar incremento del stock
    # cantidad_producto1 = detalles[1].cantidad
    assert producto.objects.get(id=producto1.id).stock == stock_anterior1 + cantidad_detalle1  #Cantidad = 3
    assert producto.objects.get(id=producto2.id).stock == stock_anterior2 + cantidad_detalle2  #Cantidad = 2


"""7. Verificar que el método get_total de una orden, devuelve el valor 
correcto de acuerdo al total de cada detalle."""

@pytest.mark.django_db
def test_get_total_orden(crear_orden):
    orden = crear_orden
    detalles = orden.detalles_orden.all()
    cantidad_producto1 = detalles[0].cantidad
    cantidad_producto2 = detalles[1].cantidad
    producto1 = detalles[0].producto
    precio_producto1 = producto1.precio
    producto2 = detalles[1].producto
    precio_producto2 = producto2.precio
    total_esperado = precio_producto1 * cantidad_producto1 + precio_producto2 * cantidad_producto2 #Get_total = 748
    total_actual = orden.get_total_orden()
    assert total_actual == total_esperado


"""8. Verificar que el método get_total_detalle de un detalle de orden,
 devuelve el valor correcto de acuerdo a al precio del producto y cantidad de la orden."""


@pytest.mark.django_db
def test_get_total_detalle(crear_orden):
    orden = crear_orden
    detalles = orden.detalles_orden.all()
    producto1 = detalles[0].producto
    precio_producto1 = producto1.precio
    producto2 = detalles[1].producto
    precio_producto2 = producto2.precio

    total_detalle1_esperado = precio_producto1 * detalles[0].cantidad  # Total_detalle = 558
    total_detalle1 = detalleorden.get_total_detalle(detalles[0])
    
    total_detalle2_esperado = precio_producto2 * detalles[1].cantidad  # Total_detalle = 190
    total_detalle2 = detalleorden.get_total_detalle(detalles[1])
    
    assert total_detalle1 == total_detalle1_esperado
    assert total_detalle2 == total_detalle2_esperado
