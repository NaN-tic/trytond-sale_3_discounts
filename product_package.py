from trytond.model import fields
from trytond.pool import PoolMeta

class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    @fields.depends('discount1', 'discount2', 'discount3', 'sale')
    def on_change_package_quantity(self):
        super().on_change_package_quantity()