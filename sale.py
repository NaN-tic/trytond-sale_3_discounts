# This file is part of sale_discount module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.config import config
DIGITS = int(config.get('digits', 'unit_price_digits', 4))
DISCOUNT_DIGITS = int(config.get('digits', 'discount_digits', 4))
_ZERO = Decimal(0)

__all__ = ['SaleLine']
__metaclass__ = PoolMeta

STATES = {
    'invisible': Eval('type') != 'line',
    'required': Eval('type') == 'line',
    }
DEPENDS = ['type']


class SaleLine:
    __name__ = 'sale.line'
    __metaclass__ = PoolMeta
    discount1 = fields.Numeric('Discount 1', digits=(16, DISCOUNT_DIGITS),
        states=STATES, depends=DEPENDS)
    discount2 = fields.Numeric('Discount 2', digits=(16, DISCOUNT_DIGITS),
        states=STATES, depends=DEPENDS)
    discount3 = fields.Numeric('Discount 3', digits=(16, DISCOUNT_DIGITS),
        states=STATES, depends=DEPENDS)

    @classmethod
    def __setup__(cls):
        super(SaleLine, cls).__setup__()
        discounts = set(['discount1', 'discount2', 'discount3'])
        cls.amount.on_change_with |= discounts
        cls.product.on_change |= discounts
        cls.quantity.on_change |= discounts
        cls.gross_unit_price.on_change |= discounts
        cls.discount.on_change |= discounts
        if hasattr(cls, 'package_quantity'):
            cls.package_quantity.on_change |= discounts

    @staticmethod
    def default_discount1():
        return 0

    @staticmethod
    def default_discount2():
        return 0

    @staticmethod
    def default_discount3():
        return 0

    def update_prices(self):
        discount1 = self.discount1 or _ZERO
        discount2 = self.discount2 or _ZERO
        discount3 = self.discount3 or _ZERO
        self.discount = 1 - ((1 - discount1) * (1 - discount2) * (1 -
                discount3))
        digits = self.__class__.discount.digits[1]
        self.discount = self.discount.quantize(Decimal(str(10.0 ** -digits)))
        res = super(SaleLine, self).update_prices()
        res['discount'] = self.discount
        return res

    @fields.depends('discount1', 'discount2', 'discount3',
        '_parent_sale.sale_discount', methods=['discount'])
    def on_change_discount1(self):
        return self.update_prices()

    @fields.depends('discount1', 'discount2', 'discount3',
        '_parent_sale.sale_discount', methods=['discount'])
    def on_change_discount2(self):
        return self.update_prices()

    @fields.depends('discount1', 'discount2', 'discount3',
        '_parent_sale.sale_discount', methods=['discount'])
    def on_change_discount3(self):
        return self.update_prices()

    def get_invoice_line(self, invoice_type):
        lines = super(SaleLine, self).get_invoice_line(invoice_type)
        for line in lines:
            line.discount1 = self.discount1
            line.discount2 = self.discount2
            line.discount3 = self.discount3
        return lines

    def _fill_line_from_kit_line(self, kit_line, line, depth):
        'Inherited from sale_kit'
        self.discount1 = _ZERO
        self.discount2 = _ZERO
        self.discount3 = _ZERO
        super(SaleLine, self)._fill_line_from_kit_line(kit_line, line, depth)
