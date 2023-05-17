# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale
from . import product_package


def register():
    Pool.register(
        sale.Move,
        sale.SaleLine,
        module='sale_3_discounts', type_='model')
    Pool.register(
        product_package.SaleLine,
        module='sale_3_discounts', type_='model', depends=['sale_product_package'])