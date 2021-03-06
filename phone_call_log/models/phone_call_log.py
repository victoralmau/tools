# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class PhoneCallLog(models.Model):
    _name = 'phone.call.log'
    _description = 'Phone Call Log'

    phone_call_log_file_id = fields.Many2one(
        comodel_name='phone.call.log.file',
        string='Phone Call Log File'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User'
    )
    number = fields.Char(
        string='Number'
    )
    duration = fields.Float(
        string='Duration'
    )
    date = fields.Datetime(
        string='Date'
    )
    type = fields.Selection(
        selection=[
            (1, 'Incoming'),
            (2, 'Outgoing'),
            (3, 'Missed'),
            (4, 'Voicemail'),
            (5, 'Rejected'),
            (6, 'Refused'),
        ],
        string='Type'
    )
    presentation = fields.Selection(
        selection=[
            (1, 'Allowed'),
            (2, 'Restricted'),
            (3, 'Unknown'),
            (4, 'Payphone'),
        ],
        string='Presentation'
    )
    contact_name = fields.Char(
        string='CONTACT NAME'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner'
    )
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead Id'
    )
    mail_activity_id = fields.Many2one(
        comodel_name='mail.activity',
        string='Mail Activity id'
    )

    @api.model
    def check_partner_id(self):
        if not self.partner_id:
            if '+' not in self.number:
                country_ids = self.env['res.country'].search(
                    [
                        ('phone_code', '=', 34)]
                )
                if country_ids:
                    code_res_country_id = country_ids[0].id
                # number
                number = self.number
            else:
                country_ids = self.env['res.country'].search(
                    [
                        ('phone_code', '=', self.number[1:3])
                    ]
                )
                if country_ids:
                    code_res_country_id = country_ids[0].id
                else:
                    country_ids = self.env['res.country'].search(
                        [
                            ('phone_code', '=', 34)
                        ]
                    )
                    if country_ids:
                        code_res_country_id = country_ids[0].id
                # number
                number = self.number[3:]
            # phone_is_mobile
            phone_is_mobile = True
            if number[0:1] != '6':
                phone_is_mobile = False
            # search
            if phone_is_mobile:
                partner_ids = self.env['res.partner'].search(
                    [
                        ('mobile_code_res_country_id', '=', code_res_country_id),
                        ('mobile', '=', number)
                    ]
                )
            else:
                partner_ids = self.env['res.partner'].search(
                    [
                        ('phone_code_res_country_id', '=', code_res_country_id),
                        ('phone', '=', number)
                    ]
                )
            # items
            if partner_ids:
                self.partner_id = partner_ids[0].id
                # check_lead_id()
                self.check_lead_id()

    @api.model
    def check_lead_id(self):
        if not self.lead_id:
            if self.partner_id:
                lead_ids = self.env['crm.lead'].search(
                    [
                        ('type', '=', 'opportunity'),
                        ('partner_id', '=', self.partner_id.id),
                        ('create_date', '<=', self.date),
                        ('date_closed', '!=', False)
                    ],
                    order="date_closed desc"
                )
                if lead_ids:
                    self.lead_id = lead_ids[0].id
                    # check_mail_activity_id()
                    self.check_mail_activity_id()
                else:
                    lead_ids = self.env['crm.lead'].search(
                        [
                            ('type', '=', 'opportunity'),
                            ('partner_id', '=', self.partner_id.id),
                            ('create_date', '<=', self.date),
                            ('date_closed', '=', False)
                        ],
                        order="create_date desc"
                    )
                    if lead_ids:
                        self.lead_id = lead_ids[0].id
                        # check_mail_activity_id()
                        self.check_mail_activity_id()

    @api.model
    def check_mail_activity_id(self):
        if self.lead_id:
            activity_type_ids = self.env['mail.activity.type'].search(
                [
                    ('is_phone_call', '=', True)
                ]
            )
            if activity_type_ids:
                # model (crm.lead)
                ir_model_ids = self.env['ir.model'].sudo().search(
                    [
                        ('model', '=', 'crm.lead')
                    ]
                )
                if ir_model_ids:
                    # search
                    mail_activity_ids = self.env['mail.activity'].search(
                        [
                            ('activity_type_id', '=', activity_type_ids[0].id),
                            ('res_model_id', '=', ir_model_ids[0].id),
                            ('res_id', '=', self.lead_id.id),
                            ('date_done', '=', self.date)
                        ]
                    )
                    if mail_activity_ids:
                        self.mail_activity_id = mail_activity_ids[0].id
                    else:
                        # vals
                        vals = {
                            'activity_type_id': activity_type_ids[0].id,
                            'date_deadline': self.date,
                            'date_done': self.date,
                            'user_id': self.user_id.id,
                            'res_model_id': ir_model_ids[0].id,
                            'res_id': self.lead_id.id,
                            'res_name': self.lead_id.name,
                            'duration': self.duration,
                            'automated': True,
                            'done': True,
                            'active': False,
                            'phone_call_type': self.type
                        }
                        # create
                        activity_obj = self.env['mail.activity'].sudo(
                            self.user_id
                        ).create(vals)
                        # update mail_message_id
                        self.mail_activity_id = activity_obj.id

    @api.model
    def operations_item(self):
        self.check_partner_id()

    @api.model
    def create(self, values):
        res = super(PhoneCallLog, self).create(values)
        res.operations_item()
        return res
