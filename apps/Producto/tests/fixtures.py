import pytest
from django.contrib.auth import get_user_model
# from apps.producto.models import Producto, Orden, DetalleOrden
from ..models import detalleorden, producto, orden

User = get_user_model()
def create_user(username, first_name='Admin', last_name='Root', email=None, *, is_active=True):
    user, created = User.objects.get_or_create(
        username=username,
        email='{}@root.com'.format(username) if email is None else email,
        defaults=dict(
            first_name=first_name,
            last_name=last_name,
            password='password',
            is_active=is_active
        )
    )
    return user


@pytest.fixture(scope='session')
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def get_default_test_user():
    test_user = create_user(username='test_user', first_name='Test', last_name='User', email='tests@user')
    return test_user


@pytest.fixture
def crear_producto():

    producto1 = producto.objects.create(nombre='Test-Producto1',precio=170, stock=10,)
    return producto1
    # producto, creado= Producto.objects.get_or_create(nombre='Test-Producto1', precio=170, stock=10)
    # return producto


@pytest.fixture
def crear_ordenvacia():

    orden1 = orden.objects.get_or_create(
        id='1',
        fecha_hora='2023-06-21T17:44:35.070168')
    return orden1

@pytest.fixture
def crear_productos():
    # RECORDAD QUE EL METODO --> GET_OR_CREATE, DEVUELVE UNA TUPLA (PRODUCTO, ESTADO(TRUE/FALSE)),
    # ENTONCES, AGREGAMOS EL DATO DEL ESTADO EN CREADO1, CREADO2
    producto1, creado1 = producto.objects.get_or_create(
        nombre='Test-Producto1',
        precio=186,
        stock=10,
    )
    producto2, creado2 = producto.objects.get_or_create(
        nombre='Test-Producto2',
        precio=95,
        stock=20,
    )
    return producto1, producto2



@pytest.fixture
def crear_orden(crear_productos):
    orden1, creado = orden.objects.get_or_create()
    producto1, producto2 = crear_productos
    detalle1, creado_detalle1 = detalleorden.objects.get_or_create(
        orden=orden1,
        cantidad=3,
        producto=producto1
    )
    detalle2, creado_detalle2 = detalleorden.objects.get_or_create(
        orden=orden1,
        cantidad=2,
        producto=producto2
    )
    # orden.detalles_orden.add(detalle1,detalle2)
    return orden1


@pytest.fixture
def crear_detalles_orden(crear_productos):
    # RECORDAD QUE EL METODO --> GET_OR_CREATE, DEVUELVE UNA TUPLA (PRODUCTO, ESTADO(TRUE/FALSE)),
    # ENTONCES, AGREGAMOS EL DATO DEL ESTADO EN CREADO1, CREADO2
    orden1, creado = orden.objects.get_or_create()
    producto1, producto2 = crear_productos
    detalle1, creado_detalle1 = detalleorden.objects.get_or_create(
        orden=orden1,
        cantidad=3,
        producto=producto1
    )
    detalle2, creado_detalle2 = detalleorden.objects.get_or_create(
        orden=orden1,
        cantidad=2,
        producto=producto2
    )
    # orden.detalles_orden.add(detalle1,detalle2)
    return detalle1,detalle2
