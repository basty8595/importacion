from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Pedido
from .forms import PedidoForm

def importacion(request):
    costo_envio_clp = 0
    total_pedido_clp = 0
    tasa_aduana_clp = 0
    iva_clp = 0
    total_impuesto_aduana_clp = 0
    costo_total_clp = 0
    costo_total_usd = 0
    costo_total_impuesto = 0
    

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            importacion = form.save(commit=False)
            


            if importacion.cantidad_unidades <= 0:
                return render(request, 'importacion.html', {'form': form, 'error_message': 'La cantidad de unidades debe ser mayor que 0'})

            if not importacion.costo_unitario_usd or not importacion.nombre_articulo or not importacion.codigo_articulo or not importacion.nombre_proveedor:
                return render(request, 'importacion.html', {'form': form, 'error_message': 'Todos los campos son requeridos'})

            importacion.total_pedido_usd = Decimal(importacion.cantidad_unidades) * Decimal(importacion.costo_unitario_usd)
            importacion.total_pedido_clp = importacion.total_pedido_usd * Decimal('890')
            importacion.costo_envio_clp = importacion.costo_envio_usd * Decimal('890')

            valor_cif_usd = importacion.total_pedido_usd + Decimal(importacion.costo_envio_usd)

            importacion.impuesto_aduana_clp = (valor_cif_usd * Decimal('0.06')) * Decimal('890')
            importacion.iva_clp = (valor_cif_usd * Decimal('0.19')) * Decimal('890')
            importacion.costo_total_impuesto = importacion.impuesto_aduana_clp + importacion.iva_clp

            
            importacion.costo_total_clp = importacion.total_pedido_clp + importacion.costo_total_impuesto + importacion.costo_envio_clp
            importacion.costo_total_usd = importacion.costo_total_clp / Decimal('890')
            
            

            importacion.save()

    else:
        form = PedidoForm()

    pedidos = Pedido.objects.all()
    data = {
    'form': form,
    'pedidos': pedidos,
    'total_pedido_clp': total_pedido_clp,
    'tasa_aduana_clp': tasa_aduana_clp,
    'iva_clp': iva_clp,
    'total_impuesto_aduana_clp': total_impuesto_aduana_clp,
    'costo_total_clp': costo_total_clp,
    'costo_total_usd': costo_total_usd,
    'costo_envio_clp': costo_envio_clp,
    'costo_total_impuesto': costo_total_impuesto
    
    
}

    return render(request, 'importacion.html',data )


def borrar_todo(request):

    Pedido.objects.all().delete()
    return redirect('importacion')