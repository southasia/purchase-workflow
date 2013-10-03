#  -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-2013 Camptocamp (<http://www.camptocamp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields
from tools.translate import _
        

class product_template(osv.osv):
    _inherit = "product.template"

    _columns = {
        'landed_cost_type': fields.selection(
            [('value','Value'),
             ('per_unit','Quantity'),
             ('none','None')],
            'Distribution Type',
            help="Used if this product is landed costs: "
                 "If landed costs are defined for purchase orders or pickings, "
                 "this indicates how the costs are distributed to the lines"),
        'landed_cost': fields.boolean(
            'Calculate Landed Costs',
            help="Check this if you want to use landed cost calculation "
                 "for average price for this product"), 
    }

    _defaults = {
        'landed_cost_type': lambda self, cr, uid, context: 
            context['landed_cost_type'] if 'landed_cost_type'\
                in context else None
    } 


class product_product(osv.osv):
    _inherit = "product.product"

    def _choose_exp_account_from(self, cr, uid, product, fiscal_position=False,
             context=None):
        """Method to compute the expense account to chose based on product and 
        fiscal position. Used in invoice creation and on_change of landed costs.
        Taken from method : _choose_account_from_po_line of purchase.py in 
        purchase module."""
        fiscal_obj = self.pool.get('account.fiscal.position')
        property_obj = self.pool.get('ir.property')
        if product:
            acc_id = product.property_account_expense.id
            if not acc_id:
                acc_id = product.categ_id.property_account_expense_categ.id
            if not acc_id:
                raise osv.except_osv(
                    _('Error!'),
                    _('Define expense account for this company: "%s" (id:%d).') 
                        % (product.name, product.id,))
        else:
            acc_id = property_obj.get(cr, uid, 
                'property_account_expense_categ', 'product.category').id
        return fiscal_obj.map_account(cr, uid, fiscal_position, acc_id)

class product_category(osv.osv):
    _inherit = 'product.category'
    _columns = {
        'landed_cost': fields.boolean(
            'Calculate Landed Costs',
            help="Check this if you want to use landed cost calculation for "
                 "average price for this catgory"),
    }

