# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class GeneratorPlanningReport(models.TransientModel):
    _name = 'generator.planning.report'
    _description = 'Generator Planning Report'

    maintenance_request_id = fields.Many2one('maintenance.request', string='Maintenance Request')

    def print_generator_planning_report(self):
        generators = []
        res = {}
        data = {}
        generator_data = {}
        non_generators_list = []
        non_generators = []
        if self.maintenance_request_id and self.maintenance_request_id.checklist_ids:
            maintenance_request_question_lines = self.env['check.list.question.line'].sudo().search(
                [('technical_inspection_id.maintenance_id', '=', self.maintenance_request_id.id)])
            for question_line in maintenance_request_question_lines:
                if question_line.generator_id and question_line.generator_id.id not in generators:
                    generators.append(question_line.generator_id.id)
                if not question_line.generator_id and question_line.id not in non_generators_list:
                    non_generators_list.append(question_line.id)
            for generator in generators:
                generator_obj = self.env['site.generator'].sudo().browse(generator)
                question_lines = self.env['check.list.question.line'].sudo().search(
                    [('generator_id', '=', generator),
                     ('technical_inspection_id.maintenance_id', '=', self.maintenance_request_id.id)])
                generator_data[generator_obj.name] = []
                category_questions = []
                for question_line in question_lines:
                    if question_line.checklist_question_id.name not in category_questions:
                        answer = ''
                        if question_line.yes_answer:
                            answer = 'Yes'
                        elif question_line.no_answer:
                            answer = 'No'
                        generator_data[generator_obj.name].append(
                            {question_line.checklist_question_id.name: {
                                answer: question_line.comment if question_line.comment else ''}})
                        category_questions.append(question_line.checklist_question_id.name)
            for non_generator in non_generators_list:
                question_lines = self.env['check.list.question.line'].sudo().browse(non_generator)
                for question_line in question_lines:
                    if question_line.checklist_question_id:
                        answer = ''
                        if question_line.yes_answer:
                            answer = 'Yes'
                        elif question_line.no_answer:
                            answer = 'No'
                        non_generators.append(
                            {question_line.checklist_question_id.name: {
                                answer: question_line.comment if question_line.comment else ''}})

        res['generators'] = generator_data
        res['non_generators'] = non_generators
        data['data'] = res
        return self.env.ref('ejaf_maintenance_planning_reports.maintenance_generators_report').report_action(self,
                                                                                                             data=data)
