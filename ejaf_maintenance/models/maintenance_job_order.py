from odoo import models, fields, api, exceptions
from odoo import tools, _
from odoo.exceptions import ValidationError


class MaintenanceJobOrder(models.Model):
    _name = 'maintenance.job.order'
    _description = "Job Order"
    _inherit = 'mail.thread'

    @api.model
    def _default_picking_type_id(self):
        picking_type = self.env['stock.picking.type'].search(
            [('company_id', '=', self.env.company.id), ('code', '=', 'outgoing')], limit=1)
        return picking_type.id

    name = fields.Char(string="Job Order NO", required=True, default='/', copy=False, index=True)
    state = fields.Selection(string="State", selection=[('draft', 'draft'),
                                                        ('inspection', 'inspection'),
                                                        ('repairing', 'repairing'),
                                                        ('done', 'done')
                                                        ], default='draft', tracking=True)
    sp_replaced = fields.Char(string="S.P. Replaced/which management")
    sla = fields.Char(string="SLA")
    oosal_duration = fields.Char(string="OOSAL Duration")
    vol = fields.Char(string="Vol")
    invol = fields.Char(string="InVol")
    flm_action = fields.Char(string="FLM Action")
    flm_comment = fields.Char(string="FLM Comment")
    problem_root_cause = fields.Char(string="Problem Root Cause")
    outage_type_id = fields.Many2one(comodel_name="outage.type", string="Outage Type", required=False, )
    other_outrage_reason = fields.Char(string="OTHER' Outage's Reason")
    delivery_ids = fields.One2many(comodel_name="stock.picking", inverse_name="job_order_id", string="Delivery Orders")
    spare_part_ids = fields.One2many(comodel_name="spare.part", inverse_name="job_order_id", string="Spare Part")
    timesheet_ids = fields.One2many(comodel_name="maintenance.timesheet", inverse_name="job_order_id")
    work_done_ids = fields.One2many(comodel_name="maintenance.work.done", inverse_name="job_order_id")
    total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost", store=True)
    default_picking_type_id = fields.Many2one(comodel_name="stock.picking.type", default=_default_picking_type_id)
    customer_complain = fields.Text(required=False)
    equipment_id = fields.Many2one('maintenance.equipment', string='Site', required=True)
    maintenance_id = fields.Many2one('maintenance.request', string='Maintenance', required=True)
    maintenance_team_id = fields.Many2one('maintenance.team', string='Maintenance Team')
    technical_inspection_ids = fields.One2many(comodel_name="technical.inspection", inverse_name="job_order_id")
    technical_inspection_count = fields.Integer(compute='_compute_technical_inspection_count')
    site = fields.Char(string="Site ID", related="equipment_id.site")
    effected_sites_no = fields.Integer(string="no. Effected sites", related="equipment_id.effected_sites_no")
    effected_sites_cell = fields.Char(string="no. of effected cells", related="equipment_id.effected_sites_cell")
    bsc_name = fields.Char(string=" BSC name", related="equipment_id.bsc_name")
    no_for_ericsson = fields.Char(string="TG. No for Ericsson", related="equipment_id.no_for_ericsson")
    bcf_no = fields.Char(string="BCF No.", related="equipment_id.bcf_no")
    region_id = fields.Many2one(comodel_name="region", string="Region", related="equipment_id.region_id")

    @api.depends('technical_inspection_ids')
    def _compute_technical_inspection_count(self):
        for record in self:
            record.technical_inspection_count = len(
                record.technical_inspection_ids) if record.technical_inspection_ids else 0.0

    @api.depends('timesheet_ids', 'timesheet_ids.cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum([line.cost for line in record.timesheet_ids]) if record.timesheet_ids else 0.0

    @api.model
    def create(self, values):
        if not values.get('name') or values.get('name') == '/':
            values['name'] = self.env['ir.sequence'].next_by_code('maintenance.job.order')
        return super(MaintenanceJobOrder, self).create(values)

    def button_start_inspection(self):
        for record in self:
            record.state = 'inspection'

    def button_start_repairing(self):
        for record in self:
            record.state = 'repairing'
            if not record.timesheet_ids:
                record.timesheet_ids = [(0, 0, {'order_check_in': fields.Datetime.now(),
                                                'name': 'Repairing Start'})]

    def create_technical_inspection(self):
        ti_obj = self.env['technical.inspection']
        checklist = self.env['check.list'].search([('maintenance_team_id', '=', self.maintenance_team_id.id)], limit=1)
        if checklist and checklist.check_list_question_ids:
            for record in self:
                technical_inspection_id = ti_obj.create({'job_order_id': record.id,
                                                         'equipment_id': record.equipment_id.id,
                                                         'maintenance_id': record.maintenance_id.id,
                                                         'check_list_id': checklist.id})
                return {
                    "type": "ir.actions.act_window",
                    "res_model": "technical.inspection",
                    "views": [[self.env.ref('ejaf_maintenance.ti_form_view').id, "form"]],
                    "res_id": technical_inspection_id.id,
                }
        else:
            raise ValidationError(_("You must Determine Check list With Questions for this maintenance Team first"))

    def action_view_technical_inspections(self):
        return {
            'name': _('Technical Inspections'),
            'res_model': 'technical.inspection',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('ejaf_maintenance.ti_tree_view').id, 'tree'),
                (self.env.ref('ejaf_maintenance.ti_form_view').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'domain': [('job_order_id', '=', self.id)],
        }

    def action_done(self):
        for record in self:
            record.state = 'done'
            if any(pick.state == 'draft' for pick in record.delivery_ids):
                raise ValidationError(_("You cant mark this order as done as there is Delivery orders in draft state "))
            record.sudo().timesheet_ids.write({'order_check_out': fields.Datetime.now()})

        return
