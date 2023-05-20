from rest_framework import routers
from apps.Producto import api

# Initializar el router de DRF solo una vez
router = routers.DefaultRouter()
# Registrar un ViewSet
router.register(prefix='producto', viewset=api.ProductoViewSet)

router.register(prefix='orden', viewset=api.OrdenViewSet)

router.register(prefix='detalleorden', viewset=api.DetalleOrdenViewSet)