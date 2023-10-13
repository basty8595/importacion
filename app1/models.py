from django.db import models
from decimal import Decimal



class Pedido(models.Model):
    cantidad_unidades = models.PositiveIntegerField()
    costo_unitario_usd = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_articulo = models.CharField(max_length=255)
    codigo_articulo = models.CharField(max_length=50)
    nombre_proveedor = models.CharField(max_length=255)
    costo_envio_usd = models.DecimalField(max_digits=10, decimal_places=2)
    
    total_pedido_clp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_pedido_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_envio_clp = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    impuesto_aduana_clp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    iva_clp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    costo_total_impuesto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    costo_total_clp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_total_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    

def save(self, *args, **kwargs):
        if self.total_pedido_usd is not None:
            self.total_pedido_clp = Decimal(self.total_pedido_usd) * Decimal('890')
            valor_cif_usd = Decimal(self.total_pedido_usd) + Decimal(self.costo_envio_usd)
            self.impuesto_aduana_clp = valor_cif_usd * Decimal('0.06') * Decimal('890')
            self.iva_clp = valor_cif_usd * Decimal('0.19') * Decimal('890')
            self.costo_total_clp = self.total_pedido_clp + self.costo_envio_usd * Decimal('890') + self.impuesto_aduana_clp
            self.costo_total_usd = self.costo_total_clp / Decimal('890')
        super(Pedido, self).save(*args, **kwargs)