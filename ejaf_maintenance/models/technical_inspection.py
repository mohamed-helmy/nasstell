# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo import tools, _
from odoo.exceptions import ValidationError


class TechnicalInspection(models.Model):
    _name = 'technical.inspection'
    _description = "Technical Inspection"
    _inherit = 'mail.thread'

    name = fields.Char(string="Sequence", required=True, default='/',
                       copy=False, index=True)
    state = fields.Selection(string="State", selection=[('draft', 'In Progress'),
                                                        ('submitted', 'Submitted'),
                                                        ], default='draft', track_visibility='always')

    maintenance_id = fields.Many2one('maintenance.request', string='Maintenance', required=False)
    maintenance_tag = fields.Selection(
        [('fuel_planning', 'Fuel Planning'), ('generators', 'Generators'), ('full_site', 'Full Site')], string='Tag',
        related='maintenance_id.maintenance_tag')
    job_order_id = fields.Many2one(comodel_name="maintenance.job.order", string="Job Order",
                                   track_visibility='always', required=False, ondelete="cascade")
    question_line_ids = fields.One2many(comodel_name="check.list.question.line",
                                        inverse_name="technical_inspection_id")
    check_list_id = fields.Many2one(comodel_name="check.list", string="CheckList")

    site_before_attach_ids = fields.Many2many('ir.attachment', 'sit_att_rel', 'ti_id', 'attach_id',
                                              string='Attachments', tracking=True, readonly=True,
                                              states={'draft': [('readonly', False)]})

    site_after_attach_ids = fields.Many2many('ir.attachment', 'sit_after_att_rel', 'ti_id', 'attach_id',
                                             string='Attachments', tracking=True, readonly=True,
                                             states={'draft': [('readonly', False)]})

    user_signature = fields.Binary(string='Signature')
    equipment_id = fields.Many2one('maintenance.equipment', string='Site', required=True)
    time_in = fields.Datetime()
    time_out = fields.Datetime()
    start_date = fields.Date()
    finish_date = fields.Date()
    contact = fields.Char()

    @api.model
    def create(self, values):
        if not values.get('name') or values.get('name') == '/':
            values['name'] = self.env['ir.sequence'].next_by_code('technical.inspection')
        result = super(TechnicalInspection, self).create(values)
        question_line = self.env['check.list.question.line']
        if result.check_list_id and result.check_list_id.check_list_question_ids:
            for question in result.check_list_id.check_list_question_ids:
                question_line.create({
                    'checklist_question_id': question.id,
                    'technical_inspection_id': result.id,
                })

        return result

    @api.constrains('question_line_ids')
    def _check_comment(self):
        for record in self:
            if any((not question.comment) for question in record.question_line_ids if
                   (question.checklist_question_id.is_comment_required and question.no_answer)):
                raise ValidationError(_("please comment to question with no answer"))

    def action_submit(self):
        for record in self:
            if record.maintenance_id and record.maintenance_id.checklist_ids:
                if record.maintenance_id.checklist_ids.filtered(
                        lambda cc: cc.is_mandatory) and not any(
                    (question.yes_answer or question.no_answer) for question in record.question_line_ids):
                    raise ValidationError(_("You must answer at least one question"))
            if any((not question.yes_answer and not question.no_answer) for question in record.question_line_ids if
                   question.is_mandatory):
                raise ValidationError(_("You cant submit until you answer mandatory questions"))
            record.state = 'submitted'
        return True

    @api.constrains('question_line_ids')
    def _check_question_line_ids(self):
        for record in self:
            if record.question_line_ids:
                for line in record.question_line_ids:
                    if line.is_mandatory and (not line.yes_answer and not line.no_answer):
                        raise ValidationError(_('Answer for %s is required') % line.checklist_question_id.name)
