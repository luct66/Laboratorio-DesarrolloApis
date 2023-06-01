from django.contrib import admin
from django.urls import include, path
from apps.Producto.views import ModelListView
from desarrolloapi.router import router
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('model-list/', ModelListView.as_view(), name='model-list'),
    path('', TemplateView.as_view(template_name='base/home.html'), name='home'),
    # urls.py

]
