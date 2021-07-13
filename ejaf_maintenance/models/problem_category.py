from odoo import api, fields, models, _


class ProblemCategory(models.Model):
    _name = 'problem.category'
    _description = 'Problem Category'

    name = fields.Char(required=True,string='Name')
    parent_category_id = fields.Many2one('problem.category', string='Parent')
    type = fields.Selection(
        [('fiber', 'Fiber'), ('other', 'Other'), ('power', 'Power'), ('system', 'System'), ('trm', 'TRM')],
        default='fiber', string='Type')
