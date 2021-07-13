from odoo import api, fields, models, _


class SiteGenerator(models.Model):
    _name = 'site.generator'
    _rec_name = 'name'
    _description = 'Site Generator'

    name = fields.Char(string='Name', required=True)
    site_id = fields.Many2one('maintenance.equipment')
    site_name = fields.Char(string='Site Name', related='site_id.name')
    install_date = fields.Integer(string="Install Date(years)")
    kva = fields.Float(string="Capacity (KVA)")
    brand = fields.Char(string="GENERATOR BRAND")
    status = fields.Char(string="Status")
    working_hours = fields.Integer(string="Working Hours")
    control_unit = fields.Char(string="Control Unit  1")
    alternator_type_id = fields.Many2one(comodel_name="generator.alternator.type", string="Alternator type")
    canopy_status = fields.Char(string="Canopy Status")
    active = fields.Boolean(default=True)
    maintenance_requests_count = fields.Integer(compute='calc_maintenance_requests')
    alternator_model_id = fields.Many2one(comodel_name="alternator.model", string="Alternator Model", required=False, )
    alternator_nr = fields.Char(string="Alternator S/Nr", required=False, )
    engine_manufacturer_id = fields.Many2one(comodel_name="engine.manufacturer", string="Engine Manufacturer",
                                             required=False, )
    engine_model_id = fields.Many2one(comodel_name="engine.model", string="Engine Model", required=False, )
    engine_nr = fields.Char(string="Engine S/Nr", required=False, )
    gen_set_manufacturer_id = fields.Many2one(comodel_name="gen.set.manufacturer", string="Gen-Set Manufacturer",
                                              required=False, )
    alternator_manufacturer_id = fields.Many2one(comodel_name="alternator.manufacturer",
                                                 string="Alternator Manufacturer", required=False, )

    def calc_maintenance_requests(self):
        for generator in self:
            generator.maintenance_requests_count = len(
                self.env['maintenance.request'].sudo().search([('planned_generator_ids', 'in', generator.id)]))

    def action_view_maintenance_requests(self):
        for generator in self:
            site_maintenances = self.env['maintenance.request'].sudo().search(
                [('planned_generator_ids', 'in', generator.id)])
            return {
                'name': _('Maintenance Requests'),
                'res_model': 'maintenance.request',
                'view_mode': 'tree,form',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', site_maintenances.ids)],
            }
