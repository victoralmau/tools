# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields, osv
from openerp.exceptions import Warning

class IrActionsAct_url(models.Model):
    _inherit = 'ir.actions.act_url'
    
    @api.multi
    def read(self, fields=None, load='_classic_read'):
        res_items = super(IrActionsAct_url, self).read(fields, load=load)
        if load=='_classic_read':
            res_items = super(IrActionsAct_url, self).read(fields, load=load)
            key = 0
            for res_item in res_items:                
                if "intranet." in res_item['url']:
                    if "?" in res_item['url']:                                    
                        res_items[key]['url'] = res_item['url']+"&odoo_password_crypt="+self.env.user.password_crypt
                    else:
                        res_items[key]['url'] = res_item['url']+"?odoo_password_crypt="+self.env.user.password_crypt
                    
                key = key + 1
                
        return res_items                                                                                                                                              