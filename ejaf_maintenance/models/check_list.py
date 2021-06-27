# -*- coding: utf-8 -*-
from odoo import models, fields


class CheckListQuestionLine(models.Model):
    _inherit = 'check.list.question.line'

    technical_inspection_id = fields.Many2one(comodel_name="technical.inspection", string="TI",
                                              required=False)
    site_id = fields.Many2one('maintenance.equipment', related='technical_inspection_id.equipment_id')
    question_type = fields.Selection(
        [('a', 'Site/Tower needs to ground system'), ('b', 'Site gate missing or needs repairing'),
         ('c', 'Aviation light system missing or not working'), ('d', 'Base of tower, concrete element not ok'),
         ('e', 'commercial power board missing not NOK'), ('f', 'FM 200 is empty'), ('i', 'TRSM Status'),
         ('j', 'RAUS & RF & RRU & TMA missing ground')], string='Question Type',
        related='checklist_question_id.question_type')
    is_mandatory = fields.Boolean(string='Mandatory?', related='checklist_question_id.is_mandatory')
    is_comment_required = fields.Boolean(string='If answer no,comment is mandatory',
                                         related='checklist_question_id.is_comment_required')
    generator_id = fields.Many2one('site.generator', string='Generator')
    attach_ids = fields.Many2many('ir.attachment', string='Attachments')


class CheckList(models.Model):
    _inherit = 'check.list'

    maintenance_team_id = fields.Many2one('maintenance.team', string='Maintenance Team')
