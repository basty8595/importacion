from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cantidad_unidades', 'costo_unitario_usd', 'nombre_articulo', 'codigo_articulo', 'nombre_proveedor', 'costo_envio_usd']
