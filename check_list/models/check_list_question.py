# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CheckListQuestion(models.Model):
    _name = 'check.list.question'
    _description = "Check List Question"
    _order = "check_list_id, sequence"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence")
    category_id = fields.Many2one(comodel_name="check.list.category", string="Category")
    check_list_id = fields.Many2one(comodel_name="check.list", string="Check List",
                                    required=True, ondelete='cascade')
    question_type = fields.Selection(
        [('a', 'Site/Tower needs to ground system'), ('b', 'Site gate missing or needs repairing'),
         ('c', 'Aviation light system missing or not working'), ('d', 'Base of tower, concrete element not ok'),
         ('e', 'commercial power board missing not NOK'), ('f', 'FM 200 is empty'), ('i', 'TRSM Status'),
         ('j', 'RAUS & RF & RRU & TMA missing ground')], string='Question Type')
    is_mandatory = fields.Boolean(string='Mandatory?')
    is_comment_required = fields.Boolean(string='If answer no,comment is mandatory')


class CheckListQuestionLine(models.Model):
    _name = 'check.list.question.line'
    _description = "Check List Question Line"

    checklist_question_id = fields.Many2one(comodel_name="check.list.question", required=True,
                                            string="CheckList Question", ondelete='cascade')
    category_id = fields.Many2one(related="checklist_question_id.category_id", store=True)
    sequence = fields.Integer(related="checklist_question_id.sequence", store=True)
    answer = fields.Selection(string="Answer", selection=[('yes', 'Yes'), ('no', 'No')])
    yes_answer = fields.Boolean(string='Yes', default=False)
    no_answer = fields.Boolean(string='No', default=False)
    no_ok_answer = fields.Boolean(string='NoT OK', default=False)
    na_answer = fields.Boolean(string='NA', default=False)
    comment = fields.Char(string="Comment")

    @api.onchange('yes_answer', 'no_answer', 'no_ok_answer', 'na_answer')
    def _check_one_answer(self):
        for line in self:
            if line.yes_answer and (line.no_answer or line.no_ok_answer or line.na_answer):
                raise ValidationError('You should select at least one answer')
            elif line.no_answer and (line.yes_answer or line.no_ok_answer or line.na_answer):
                raise ValidationError('You should select at least one answer')
            elif line.no_ok_answer and (line.yes_answer or line.no_answer or line.na_answer):
                raise ValidationError('You should select at least one answer')
            elif line.na_answer and (line.yes_answer or line.no_answer or line.no_ok_answer):
                raise ValidationError('You should select at least one answer')
