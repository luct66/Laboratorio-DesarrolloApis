import pytest
#import self
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .fixtures import crear_productos,crear_ordenvacia, crear_orden, api_client, get_default_test_user
from ..models import detalleorden, producto, orden
import json


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

@pytest.mark.parametrize(
    'codigo_http, codigo_http_producto_repetido, codigo_http_cantidad, total_registros, loguear_usuario',
    [(201, 400, 400, 1, True)]# #Inciso 2 APROBADO al crear una orden, con dos detalles orden
     #(201, 201, 400, 1, True), #Inciso 3 FALLO al crear Producto repetido en la orden
     #(201, 400, 201, 1, True)] #Inciso 4 FALLO al haber Cantidad menor o igual al stock del producto
)

@pytest.mark.django_db
def test_api_creacion_orden(api_client, get_default_test_user, crear_ordenvacia, crear_productos,
                            codigo_http, codigo_http_producto_repetido, codigo_http_cantidad, total_registros, loguear_usuario):
    
    client = api_client
    if loguear_usuario:
        client.force_authenticate(user=get_default_test_user)

    producto1, producto2 = crear_productos

    orden1, _ = crear_ordenvacia

    #print(detalle_orden1)
    data_orden = {
        'fecha_hora': orden1.fecha_hora
    }

    data_detalle1 = {
        "orden": orden1.id,
        "cantidad": 5,
        "precio_unitario": producto1.precio,
        "producto": producto1.id,
    }

    data_detalle2 = {
        "orden": orden1.id,
        "cantidad": 3,
        "precio_unitario": producto2.precio,
        "producto": producto2.id,
    }
    data_detalle3 = {
        "orden": orden1.id,
        "cantidad": 300,
        "precio_unitario": producto2.precio,
        "producto": producto2.id,
    }
    print(data_detalle1)

    response_orden = client.post('/orden/',data=data_orden)
    response_detalle1 = client.post('/detalleorden/', data=data_detalle1)
    print(response_detalle1.content)
    response_detalle2 = client.post('/detalleorden/', data=data_detalle2)
    #Cantidad menor o igual al stock del producto
    #Producto repetido en la orden
    response_detalle4 = client.post('/detalleorden/', data=data_detalle2)
    response_detalle3 = client.post('/detalleorden/', data=data_detalle3)
    print(response_detalle3.content)
    print(response_detalle4.content)
    assert response_orden.status_code == codigo_http
    assert response_detalle1.status_code == codigo_http
    assert response_detalle2.status_code == codigo_http
    #Se espera un status_code = 400 , porque el producto ya se encuentra en la orden
    assert response_detalle3.status_code == codigo_http_cantidad
    
    assert response_detalle4.status_code == codigo_http_producto_repetido

    # Verificar que se haya creado correctamente
    assert orden.objects.filter(id=orden1.id
    ).count() == total_registros

    response = client.get(f'/orden/{orden1.id}/')
    json_data = response.json()

    print(json_data)
    assert json_data['id'] == orden1.id
    #assert json_data['fecha_hora'] == '2023-06-12T00:00:00Z'
    #assert json_data['get_total'] == 3900


# Realiza una consulta a la base de datos para obtener los valores más recientes de los campos del objeto y los actualiza en el objeto en memoria.
    producto1.refresh_from_db()
    producto2.refresh_from_db()
    #actualizado el stock del producto
    assert producto1.stock == 5
    assert producto2.stock == 17


"""

@pytest.mark.django_db
def test_api_creacion_orden(api_client, get_default_test_user,crear_productos,crear_detalles_orden):
    client = api_client
    client.force_authenticate(user=get_default_test_user)
    producto1, producto2 = crear_productos
    stock_producto1 = producto1.stock
    stock_producto2 = producto2.stock
        

    data = {
    "detalles_orden": [
        {"producto": producto1.id, "cantidad": "2"},
        {"producto": producto2.id, "cantidad": "3"}
    ]
    }

    #orden_creada = client.post('/orden/', json.dumps(data), content_type='application/json')

    orden_creada = client.post('/orden/', data, format='json')
    #orden_creada = client.get('/orden/')
    json_data = orden_creada.json()
    # Verifico la correcta creación de la orden
    print(orden_creada.content)

    assert orden_creada.status_code == status.HTTP_201_CREATED
    # Verifico la cantidad y los productos incluidos
    assert json_data['id'] is not None
    #print(orden_creada)
    
    assert json_data['detalles_orden'][0] == producto1.id
    assert detalleorden.objects.filter(producto = producto1, cantidad = 2, orden__id= json_data['id']).count() == 1
    assert json_data['detalles_orden'][1]['producto'] == producto2.id
    assert detalleorden.objects.filter(producto=producto2, cantidad=3, orden__id=json_data['id']).count() == 1
    # Verifico que se halla actualizado el stock correspondiente
    producto1.refresh_from_db(fields=['stock'])
    assert producto1.stock == stock_producto1 - 2
    producto2.refresh_from_db(fields=['stock'])
    assert producto2.stock == stock_producto2 - 3
    
    # Método 1--> Accede a la BD y recupera el stock
    # assert Producto.objects.get(pk = producto1.id).stock ==                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       - 1




@pytest.mark.django_db
@pytest.mark.parametrize("detalles_orden, producto1_id, producto2_id", [
    ([{"producto": 1, "cantidad": "2"}], 1, None),
    ([{"producto": 2, "cantidad": "3"}], None, 2),
    ([{"producto": 1, "cantidad": "2"}, {"producto": 2, "cantidad": "3"}], 1, 2),
])
def test_api_creacion_orden(api_client, get_default_test_user, crear_productos, detalles_orden, producto1_id, producto2_id):
    client = api_client
    client.force_authenticate(user=get_default_test_user)
    producto1, producto2 = crear_productos
    stock_producto1 = producto1.stock
    stock_producto2 = producto2.stock
    print(detalles_orden.copy())
    data = {
        "detalles_orden": detalles_orden.copy()  # Crear una copia de la lista detalles_orden
    }
    if producto1_id:
        data["detalles_orden"][0]["producto"] = producto1_id
    if producto2_id and len(data["detalles_orden"]) > 1:
        data["detalles_orden"][1]["producto"] = producto2_id
    orden_creada = client.post('/orden/', data=data, format='json')
    print(client)
    print(orden_creada.status_code)
    print(orden_creada.content)
    json_data = orden_creada.json()
    print(json_data)
    assert json_data['detalles_orden'][0]["producto"] == producto1.id




@pytest.mark.django_db
def test_api_creacion_orden_detalles_repetidos(api_client, get_default_test_user, crear_productos):
    client = api_client
    client.force_authenticate(user=get_default_test_user)
    producto1, producto2 = crear_productos
    data = {
        "detalles_orden": [
            {"producto": producto1.id, "cantidad": "1"},
            {"producto": producto1.id, "cantidad": "3"}
        ]
    }
    orden_creada = client.post('/orden/', data, format='json')
    json_data = orden_creada.json()
    #print(orden_creada)
    print(orden_creada.content)
    # Verifico que la orden no se halla creado
    assert orden_creada.status_code == status.HTTP_400_BAD_REQUEST
    # Verifico que la orden y el detalle no esten contenidos en la BD
    assert orden.objects.all().count() == 0
    assert detalleorden.objects.all().count() == 0



@pytest.mark.django_db
def test_api_creacion_orden_cantidad_supera_stock(api_client, get_default_test_user, crear_productos):
    client = api_client
    client.force_authenticate(user=get_default_test_user)
    producto1, producto2 = crear_productos
    data = {
        "detalles_orden": [
            {"producto": producto1.id, "cantidad": (producto1.stock + 4)},  #Stock max producto1 = 10
            {"producto": producto2.id, "cantidad": "3"}   #Stock max producto2 = 20
        ]
    }
    orden_creada = client.post('/orden/',data, format='json')
    print(orden_creada.content)
    json_data = orden_creada.json()
    # Verifico que la orden no se halla creado
    assert orden_creada.status_code == status.HTTP_400_BAD_REQUEST
    # Verifico que la orden y el detalle no esten contenidos en la BD
    assert orden.objects.all().count() == 0
    assert detalleorden.objects.all().count() == 0

"""
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
   #total_actual = orden.get_total_orden(orden)
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
    # Tomo el detalle 1
    total_detalle1_esperado = precio_producto1 * detalles[0].cantidad  # Total_detalle = 558
    total_detalle1 = detalleorden.get_total_detalle(detalles[0])
    # Tomo el detalle 2
    total_detalle2_esperado = precio_producto2 * detalles[1].cantidad  # Total_detalle = 190
    total_detalle2 = detalleorden.get_total_detalle(detalles[1])
    assert total_detalle1 == total_detalle1_esperado
    assert total_detalle2 == total_detalle2_esperado
