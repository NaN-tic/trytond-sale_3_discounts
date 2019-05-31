# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale


def register():
    Pool.register(
        sale.Move,
        sale.SaleLine,
        module='sale_3_discounts', type_='model')
