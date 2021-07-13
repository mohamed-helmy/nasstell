from odoo.exceptions import ValidationError
from odoo import api, fields, models, _
from odoo import http, modules, SUPERUSER_ID, tools, _
from datetime import timedelta


class MaintenanceType(models.Model):
    _name = 'maintenance.type'
    _description = 'Maintenance Type'

    name = fields.Selection([('corrective', 'Corrective'), ('preventive', 'Preventive'), ('emergency', 'Emergency')],
                            default='corrective', string='Maintenance Type')


class MaintenanceTag(models.Model):
    _name = 'maintenance.tag'
    _description = 'Maintenance Tag'

    name = fields.Selection(
        [('fuel_planning', 'Fuel Planning'), ('generators', 'Generators'), ('full_site', 'Full Site')],
        default='fuel_planning', string='Maintenance Tag')


class MaintenanceTeam(models.Model):
    _inherit = 'maintenance.team'

    maintenance_type_ids = fields.Many2many('maintenance.type', string='Maintenance Types')
    maintenance_tag_ids = fields.Many2many('maintenance.tag', string='Maintenance Tags')
    show_tags = fields.Boolean(default=False, copy=False)
    team_leader_id = fields.Many2one('res.users', string="Team Leader", domain="[('company_ids', 'in', company_id)]")
    is_manager = fields.Boolean(compute='check_user_is_admin')

    def check_user_is_admin(self):
        self.is_manager = True if self.env.user.has_group('base.group_erp_manager') else False

    @api.onchange('maintenance_type_ids')
    def show_maintenance_tags(self):
        for team in self:
            if team.maintenance_type_ids and team.maintenance_type_ids.filtered(lambda l: l.name == 'preventive'):
                team.show_tags = True
            else:
                team.show_tags = False


class MaintenanceRequestActivity(models.Model):
    _name = 'maintenance.request.activity'
    _description = 'Maintenance Request Activity'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')


class GeneratorRH(models.Model):
    _name = 'generator.rh'

    generator_id = fields.Many2one('site.generator', string='Generator')
    rh = fields.Char(string='RH')
    maintenance_request_id = fields.Many2one('maintenance.request', string='Maintenance Request')
    site_id = fields.Many2one('maintenance.equipment', related='maintenance_request_id.equipment_id')


class MaintenanceStage(models.Model):
    _inherit = 'maintenance.stage'

    state = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('repaired', 'Repaired'), ('scraped', 'Scrapped')],
        default='draft')


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    def _get_default_team(self):
        MT = self.env['maintenance.team']
        corrective_type = self.env['maintenance.type'].sudo().search([('name', '=', 'corrective')], limit=1)
        team = MT.sudo().search(
            [('maintenance_type_ids', 'in', [corrective_type.id]), ('company_id', '=', self.env.company.id)], limit=1)
        if team:
            return team.id
        else:
            return False

    starting_outage_time = fields.Datetime(string="Starting Outage Time", copy=False)
    starting_time = fields.Datetime(string="Start Time", copy=False)
    end_time = fields.Datetime(string="End Time", copy=False)
    site_code = fields.Char(related='equipment_id.site', string='Site ID')
    maintenance_type = fields.Selection(selection_add=[('emergency', 'Emergency')])
    closing_outage_time = fields.Datetime(string="Restoration Time")
    gov = fields.Many2one('region', string='Gov', related='equipment_id.region_id')
    effected_trxs = fields.Integer(string='Effected Trxs')
    effected_cells = fields.Integer(string='Effected Cells')
    effected_sites = fields.Integer(string='Effected Sites')
    state = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('repaired', 'Repaired'), ('scraped', 'Scrapped')],
        related='stage_id.state')
    bsc_name = fields.Char(string='BSC Name', related='equipment_id.bsc_name')
    tg_number = fields.Integer(string='TG No', related='equipment_id.tg_number')
    tt_issuer = fields.Char(string='TT Issuer')
    tt_no = fields.Char(string='TT No')
    tt_status = fields.Selection([('open', 'Open'), ('in_progress', 'In Progress'), ('closed', 'Closed')],
                                 string='TT Status', default='open')
    alarm_time = fields.Datetime(string='Alarm Time')
    ne_type_id = fields.Many2one(comodel_name="ne.type", string="NE Type", related='equipment_id.ne_type_id')
    ne_impacted_id = fields.Many2one(comodel_name="ne.impacted", string="NE Impacted",
                                     related='equipment_id.ne_impacted_id')
    tt_issuing_time = fields.Datetime(string="TT Issuing Time")
    outage_duration = fields.Float(string="Outage duration", compute="_get_outage_duration", store=True)
    outage_duration_str = fields.Char(string="Outage duration", compute="_get_outage_duration", store=True)
    duration_str = fields.Char(string="duration", compute="_get_duration_str", store=True, copy=False)
    alarm_description = fields.Text(string="Alarm description")
    route_cause = fields.Text(string="Root")
    nmc_comment = fields.Html(string="NMC Comment")
    outage_category_id = fields.Many2one(comodel_name="outage.category", string="Outage Category")
    job_order_ids = fields.One2many(comodel_name="maintenance.job.order", inverse_name="maintenance_id")
    job_order_count = fields.Integer(compute='_compute_job_order_count',
                                     store=True, compute_sudo=True)
    id_permission_time = fields.Float(string='ID Permission Time')
    id_permission_time_str = fields.Char(string='ID Permission Time', default='00:00:00')
    vol_str = fields.Char(string='Vol')
    vol_option = fields.Boolean(copy=False)
    in_vol = fields.Float(string='In-vol')
    in_vol_option = fields.Boolean(copy=False)
    in_vol_str = fields.Char(string='In-vol', default='00:00:00')
    problem_category_id = fields.Many2one('problem.category', string='Problem Category')
    sub_category_id = fields.Many2one('problem.category', string='Sub Category')
    why_it_happened = fields.Char(string='Why it happened')
    site_severity = fields.Many2one('maintenance.equipment.category', related='equipment_id.category_id',
                                    string='Site Severity')
    action_taken = fields.Char(string='Action Taken')
    any_sp_used = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Any SP Used', default='no')
    comment = fields.Char(string='Comment')
    is_team_leader = fields.Boolean(string="", compute='_cheeck_team_leader')
    technical_inspection_ids = fields.One2many('technical.inspection', 'maintenance_id', string='Technical Inspections')
    request_timeline_ids = fields.One2many('maintenance.request.timeline', 'maintenance_request_id', string='Timeline')
    origin = fields.Char(string='Origin')
    maintenance_tag = fields.Selection(
        [('fuel_planning', 'Fuel Planning'), ('generators', 'Generators'), ('full_site', 'Full Site')], string='Tag')

    timer_start = fields.Datetime("Timer Start", copy=False)
    timer_first_start = fields.Datetime("Start Date", readonly=True, copy=False)
    timer_last_stop = fields.Datetime("End Date", readonly=True, copy=False)
    starting_time = fields.Datetime(string="Start Time")
    starting_time_date = fields.Date(string="Start Time Date", compute='_calc_dates', store=1)
    end_time = fields.Datetime(string="End Time")
    duration_in_minutes = fields.Float(string='Duration', copy=False)
    timer_first_start_date = fields.Date("Start Date", compute='_calc_dates', store=1)
    checklist_ids = fields.Many2many('check.list', string='Checklists')
    maintenance_team_id = fields.Many2one('maintenance.team', string='Team', required=False,
                                          default=_get_default_team, check_company=True)
    planned_generator_ids = fields.Many2many("site.generator", string='Planned Generators')
    pm_status_first_visit = fields.Char(string='PM Status 1st Visit')
    pm_status_first_visit_date = fields.Date(string='Date')
    pm_status_second_visit = fields.Char(string='PM Status 2nd Visit')
    pm_status_second_visit_date = fields.Date(string='Date')
    generator_rh_ids = fields.One2many('generator.rh', 'maintenance_request_id', string='Generator RHs')
    status = fields.Char(string='Status')
    activity = fields.Many2many('maintenance.request.activity', string='Activity')
    remark = fields.Char(string='Remark')

    # fuel fields
    g1rh = fields.Float(string='G1RH')
    g1rh_analysis = fields.Float(string='G1RH', compute='calc_g1_rh')
    g2rh = fields.Float(string='G2RH')
    g2rh_analysis = fields.Float(string='G2RH', compute='calc_g2_rh')
    total_rhs = fields.Float(compute='calc_total_rhs', string='Total RHs')
    days = fields.Float(string='Days', compute='get_days')
    liters_per_hour = fields.Float(string='Liters Per Hour', digits=(16, 2), compute='calc_liters_per_hour')
    tank_size = fields.Float(string='Tank Size', related='equipment_id.tank_size')
    remain_letters = fields.Float(string='Remain Letters in the tank')
    liters_in_the_tank = fields.Float(string='Liters in the tank')
    c_p_status = fields.Char(string='C.P Status')
    filling_liters = fields.Float(string='Filling Liters')
    total_liters = fields.Float(compute='get_total', string='Total Liters')
    rh_per_day = fields.Float(string='R.H/Day', compute='calc_rh_per_day')
    reservation_liters = fields.Float(string='Reservation Liters', related='equipment_id.reservation_liters')
    available_for_use = fields.Float(string='Available for Use', compute='calc_available_for_use')
    remaining_days_before_next_visit = fields.Float(string='Remaining Days before next visit',
                                                    compute='calc_remaining_days_before_next_visit')
    next_visit_plan = fields.Date(string='Next Visit Plan', compute='calc_next_visit_plan',
                                  inverse='_set_next_visit_plan')
    next_visit_plan_temp = fields.Date(string='Next Visit Plan')
    timer_started = fields.Boolean()
    timer_stopped = fields.Boolean()
    member_ids = fields.Many2many('res.users', string='Team Members')

    @api.depends('g1rh', 'maintenance_type', 'equipment_id', 'maintenance_tag', 'starting_time')
    def calc_g1_rh(self):
        for request in self:
            request.g1rh_analysis = 0
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            if request.g1rh and request.maintenance_type and request.maintenance_type == 'preventive' and request.maintenance_tag and request.maintenance_tag == 'fuel_planning' and request.equipment_id and request.starting_time and request.stage_id.id == repaired_stage.id:
                before_maintenance_req_in_site = self.sudo().search(
                    [('maintenance_type', '=', 'preventive'), ('maintenance_tag', '=', 'fuel_planning'),
                     ('stage_id', '=', repaired_stage.id),
                     ('equipment_id', '=', request.equipment_id.id),
                     ('starting_time', '<', request.starting_time)],
                    order="starting_time desc", limit=1)
                request.g1rh_analysis = request.g1rh - before_maintenance_req_in_site.g1rh

    @api.depends('g2rh', 'maintenance_type', 'equipment_id', 'maintenance_tag', 'starting_time')
    def calc_g2_rh(self):
        for request in self:
            request.g2rh_analysis = 0
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            if request.g2rh and request.maintenance_type and request.maintenance_type == 'preventive' and request.maintenance_tag and request.maintenance_tag == 'fuel_planning' and request.equipment_id and request.starting_time and request.stage_id.id == repaired_stage.id:
                before_maintenance_req_in_site = self.sudo().search(
                    [('maintenance_type', '=', 'preventive'), ('equipment_id', '=', request.equipment_id.id),
                     ('maintenance_tag', '=', 'fuel_planning'),
                     ('starting_time', '<', request.starting_time), ('stage_id', '=', repaired_stage.id)],
                    order="starting_time desc", limit=1)
                request.g2rh_analysis = request.g2rh - before_maintenance_req_in_site.g2rh

    @api.depends('end_time', 'remaining_days_before_next_visit')
    def calc_next_visit_plan(self):
        for request in self:
            if request.next_visit_plan_temp:
                request.next_visit_plan = request.next_visit_plan_temp
            else:
                repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
                request.next_visit_plan = (request.end_time + timedelta(
                    days=int(
                        request.remaining_days_before_next_visit))) if request.end_time and request.stage_id.id == repaired_stage.id else False

    @api.onchange('next_visit_plan')
    def _set_fuel_date(self):
        for request in self:
            fuel_lines = self.env['fuel.planning.line'].sudo().search(
                [('site_id', '=', request.equipment_id.id), ('maintenance_request_id', '=', self._origin.id)])
            planning_ids = []
            for line in fuel_lines:
                if line.plan_id.id not in planning_ids:
                    planning_ids.append(line.plan_id.id)
            for plan in planning_ids:
                self.env['fuel.planning.line'].sudo().create({'plan_id': plan,
                                                              'site_id': request.equipment_id.id,
                                                              'date': request.next_visit_plan,
                                                              'maintenance_team_id': request.maintenance_team_id.id})

    def _set_next_visit_plan(self):
        for request in self:
            request.next_visit_plan_temp = request.next_visit_plan

    @api.depends('tank_size', 'remain_letters', 'liters_per_hour', 'rh_per_day')
    def calc_remaining_days_before_next_visit(self):
        for req in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            first_part = (
                    req.tank_size / req.remain_letters) if req.remain_letters and req.stage_id.id == repaired_stage.id else 0
            req.remaining_days_before_next_visit = (first_part / (req.liters_per_hour * req.rh_per_day)) if (
                    req.liters_per_hour * req.rh_per_day) else 0

    @api.depends('tank_size', 'reservation_liters')
    def calc_available_for_use(self):
        for record in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            record.available_for_use = (
                    record.tank_size - record.reservation_liters) if record.stage_id.id == repaired_stage.id else 0

    @api.depends('total_rhs', 'days')
    def calc_rh_per_day(self):
        for record in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            record.rh_per_day = (
                    record.total_rhs / record.days) if record.days and record.stage_id.id == repaired_stage.id else 0

    @api.depends('filling_liters', 'total_rhs')
    def calc_liters_per_hour(self):
        for maintenance in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            maintenance.liters_per_hour = (
                    maintenance.filling_liters / maintenance.total_rhs) if maintenance.total_rhs and maintenance.stage_id.id == repaired_stage.id else 0

    @api.depends('g1rh_analysis', 'g2rh_analysis')
    def calc_total_rhs(self):
        for request in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            request.total_rhs = (
                    request.g1rh_analysis + request.g2rh_analysis) if request.stage_id.id == repaired_stage.id else 0

    @api.depends('liters_in_the_tank', 'filling_liters')
    def get_total(self):
        for maintenance in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            maintenance.total_liters = (
                    maintenance.liters_in_the_tank + maintenance.filling_liters) if maintenance.stage_id.id == repaired_stage.id else 0

    @api.depends('equipment_id', 'starting_time')
    def get_days(self):
        for request in self:
            repaired_stage = self.env['maintenance.stage'].sudo().search([('done', '=', True)], limit=1)
            before_maintenance_req_in_site = self.env['maintenance.request'].sudo().search(
                [('maintenance_type', '=', 'preventive'), ('equipment_id', '=', request.equipment_id.id),
                 ('maintenance_tag', '=', 'fuel_planning'),
                 ('starting_time', '<', request.starting_time), ('stage_id', '=', repaired_stage.id)],
                order="starting_time desc", limit=1)
            diff_days = (
                                request.starting_time - before_maintenance_req_in_site.starting_time).days + 1 if request.starting_time and before_maintenance_req_in_site and before_maintenance_req_in_site.starting_time and request.starting_time >= before_maintenance_req_in_site.starting_time else 0
            request.days = diff_days if request.stage_id.id == repaired_stage.id else False

    @api.onchange('maintenance_tag', 'equipment_id')
    def set_planned_generators(self):
        for request in self:
            if request.equipment_id and request.maintenance_tag == 'generators':
                site_generators = self.env['site.generator'].sudo().search([('site_id', '=', request.equipment_id.id)])
                request.planned_generator_ids = site_generators.ids

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        super(MaintenanceRequest, self).onchange_equipment_id()
        self.user_id = False

    @api.onchange('category_id')
    def onchange_category_id(self):
        super(MaintenanceRequest, self).onchange_category_id()
        self.user_id = False

    @api.onchange('maintenance_type', 'maintenance_tag')
    @api.depends('maintenance_type', 'maintenance_tag')
    def set_maintenance_team_domain(self):
        for request in self:
            teams = False
            if request.maintenance_type:
                request.maintenance_team_id = False
                maintenance_type_obj = self.env['maintenance.type'].sudo().search(
                    [('name', '=', request.maintenance_type)], limit=1)
                if request.maintenance_type == 'preventive' and request.maintenance_tag:
                    maintenance_tag_obj = self.env['maintenance.tag'].sudo().search(
                        [('name', '=', request.maintenance_tag)], limit=1)
                    teams = self.env['maintenance.team'].sudo().search(
                        [('maintenance_type_ids', 'in', [maintenance_type_obj.id]),
                         ('maintenance_tag_ids', 'in', [maintenance_tag_obj.id]),
                         ('company_id', '=', self.company_id.id)])
                else:
                    teams = self.env['maintenance.team'].sudo().search(
                        [('maintenance_type_ids', 'in', [maintenance_type_obj.id]),
                         ('company_id', '=', self.company_id.id)])
            teams_arr = teams.ids if teams else []
            request.maintenance_team_id = teams[0].id if teams else False
            return {'domain': {
                'maintenance_team_id': [('id', 'in', teams_arr)]
            }}

    @api.onchange('maintenance_team_id')
    def set_maintenance_members_domain(self):
        for request in self:
            member_arr = []
            if request.maintenance_team_id:
                request.member_ids = False
                member_arr = request.maintenance_team_id.member_ids.ids
                if request.maintenance_team_id.team_leader_id:
                    member_arr.append(request.maintenance_team_id.team_leader_id.id)
            return {'domain': {
                'member_ids': [('id', 'in', member_arr), ('company_id', '=', self.company_id.id)],
                'user_id': [('id', 'in', member_arr), ('company_id', '=', self.company_id.id)]
            }}

    @api.constrains('checklist_ids')
    def _check_technical_inspection(self):
        for request in self:
            if request.checklist_ids:
                # create questions
                ti_obj = self.env['technical.inspection']
                question_line = self.env['check.list.question.line']
                maintenance_inspection = ti_obj.sudo().search([('maintenance_id', '=', request.id)])
                if not maintenance_inspection:
                    technical_inspection_id = ti_obj.create({
                        'equipment_id': request.equipment_id.id if request.equipment_id else False,
                        'maintenance_id': request.id})
                    for checklist in request.checklist_ids:
                        for question in checklist.check_list_question_ids:
                            question_line.create({
                                'checklist_question_id': question.id,
                                'technical_inspection_id': technical_inspection_id.id,
                            })
                else:
                    checklist_questions = []
                    technical_questions = []
                    technical_inspection_id = maintenance_inspection[0]
                    for checklist in request.checklist_ids:
                        for question in checklist.check_list_question_ids:
                            if question.id not in checklist_questions:
                                checklist_questions.append(question.id)
                            for qq in technical_inspection_id.question_line_ids:
                                if qq.checklist_question_id.id not in technical_questions:
                                    technical_questions.append(qq.checklist_question_id.id)
                        diff = list(set(checklist_questions) - set(technical_questions))
                        for question_id in diff:
                            question_line.create({
                                'checklist_question_id': question_id,
                                'technical_inspection_id': technical_inspection_id.id,
                            })

    @api.onchange('maintenance_tag')
    def set_checklists(self):
        for record in self:
            if record.maintenance_tag:
                checklists = self.env['check.list'].sudo().search(
                    [('type', '=', record.maintenance_tag), ('is_default', '=', True),
                     ('company_id', '=', self.env.company.id)])
                record.checklist_ids = [(6, 0, checklists.ids)]

    @api.depends('timer_first_start', 'starting_time')
    def _calc_dates(self):
        for rec in self:
            rec.timer_first_start_date = rec.timer_first_start.date() if rec.timer_first_start else False
            rec.starting_time_date = rec.starting_time.date() if rec.starting_time else False


    def reset_equipment_request(self):
        res = super(MaintenanceRequest, self).reset_equipment_request()
        self.write({
            'timer_started': False,
            'timer_stopped': False,
        })
        return res

    def write(self, vals):
        res = super(MaintenanceRequest, self).write(vals)
        if vals.get('maintenance_team_id', False):
            for request in self:
                if request.maintenance_team_id and request.maintenance_team_id.team_leader_id:
                    request.user_id = request.maintenance_team_id.team_leader_id.id
                    user = request.maintenance_team_id.team_leader_id
                    partner_ids = [user.partner_id.id]
                    if request.member_ids:
                        for member in request.member_ids:
                            if member.partner_id.id not in partner_ids:
                                partner_ids.append(member.partner_id.id)
                    request.message_notify(
                        partner_ids=partner_ids,
                        subject=_('Check the maintenance request [%s] for the planning date %s') % (
                            request.name, request.request_date),
                        message_type='email',
                        subtype='mt_comment',
                    )
        return res

    @api.model
    def create(self, values):
        draft_stage = self.env['maintenance.stage'].sudo().search([('state', '=', 'draft')])
        values['stage_id'] = draft_stage[0].id if draft_stage else False
        return super(MaintenanceRequest, self).create(values)

    def action_need_to_repaired(self):
        for request in self:
            draft_stage = self.env['maintenance.stage'].sudo().search([('state', '=', 'draft')])
            request.stage_id = draft_stage[0].id if draft_stage else False
            request.timer_started = False
            request.timer_stopped = False
            if request.technical_inspection_ids:
                technical_inspections = self.env['technical.inspection'].sudo().browse(
                    request.technical_inspection_ids._origin.ids)
                for technical in technical_inspections:
                    technical.state = 'draft'

    def action_reviewed(self):
        for request in self:
            done_stage = self.env['maintenance.stage'].sudo().search([('state', '=', 'repaired')])
            request.stage_id = done_stage.id

    @api.onchange('problem_category_id', 'problem_category_id.type')
    def _check_vol_and_in_vol_option(self):
        for request in self:
            if request.problem_category_id and request.problem_category_id.type in ['fiber', 'other']:
                request.in_vol_option = True
                request.vol_option = False
            else:
                request.vol_option = True
                request.in_vol_option = False

    def _cheeck_team_leader(self):
        for rec in self:
            rec.is_team_leader = True if rec.maintenance_team_id.team_leader_id.id == self.env.user.id else False

    @api.onchange('in_vol_option', 'vol_option', 'outage_duration_str')
    def _check_vol_and_in_vol(self):
        for maintenance in self:
            if maintenance.vol_option and maintenance.in_vol_str != '00:00:00':
                maintenance.in_vol_option = False
            elif maintenance.in_vol_option and maintenance.vol_str != '00:00:00':
                maintenance.vol_option = False
            if maintenance.vol_option and maintenance.vol_option and maintenance.outage_duration_str:
                maintenance.vol_str = maintenance.outage_duration_str if maintenance.outage_duration_str else '00:00:00'
            else:
                maintenance.vol_str = '00:00:00'
            if maintenance.in_vol_option and maintenance.in_vol_option and maintenance.outage_duration_str:
                maintenance.in_vol_str = maintenance.outage_duration_str if maintenance.outage_duration_str else '00:00:00'
                maintenance.vol_option = False
            else:
                maintenance.in_vol_str = '00:00:00'

    @api.onchange('sub_category_id')
    def set_parent_category(self):
        for record in self:
            if record.sub_category_id and record.sub_category_id.parent_category_id:
                record.problem_category_id = record.sub_category_id.parent_category_id.id

    def action_timer_start(self):
        self.ensure_one()
        self.timer_started = True
        self.timer_stopped = False
        if not self.timer_first_start:
            self.write({'timer_first_start': fields.Datetime.now()})
        stage = self.env['maintenance.stage'].sudo().search([('state', '=', 'in_progress')], limit=1)
        self.write({'timer_start': fields.Datetime.now(), 'stage_id': stage.id, 'user_id': self.env.user.id})
        now = fields.Datetime.now()
        vals = {'tt_status': 'in_progress'}
        if not self.starting_time:
            vals.update({
                'starting_time': now
            })
        if not self.starting_outage_time:
            vals.update({
                'starting_outage_time': now
            })
        if not self.timer_start:
            vals.update({
                'timer_start': now
            })
        self.write(vals)
        self.env['maintenance.request.timeline'].create({
            'maintenance_request_id': self.id,
            'start_time': now
        })

    def action_timer_stop(self):
        self.ensure_one()
        if self.maintenance_type in ['corrective', 'emergency']:
            if not self.route_cause:
                raise ValidationError('Route cause is required before stop')
            if not self.why_it_happened:
                raise ValidationError('Why it happened is required before stop')
            if not self.action_taken:
                raise ValidationError('Action taken is required before stop')
            if not self.any_sp_used:
                raise ValidationError('Any sp used is required before stop')

        maintenance_technical_inspections = False
        if self.checklist_ids and self.checklist_ids.filtered(
                lambda cc: cc.is_mandatory):
            maintenance_technical_inspections = self.env['technical.inspection'].sudo().search(
                [('maintenance_id', '=', self.id)])
        if maintenance_technical_inspections and not any(
                (question.yes_answer or question.no_answer) for question in
                maintenance_technical_inspections.question_line_ids):
            raise ValidationError(_("You must answer at least one question"))
        self.timer_stopped = True
        start_time = self.timer_start
        if start_time:  # timer was either running or paused
            minutes_spent = round((fields.Datetime.now() - start_time).total_seconds() / 60, 2)
            self.write({'timer_last_stop': fields.Datetime.now(), 'duration_in_minutes': minutes_spent,
                        'duration': minutes_spent * 60 / 3600})
        stage = self.env['maintenance.stage'].sudo().search([('state', '=', 'repaired')], limit=1)
        self.write({'stage_id': stage.id})

        start_time = self.timer_start
        if start_time:  # timer was either running or paused
            now = fields.Datetime.now()
            self.write({'closing_outage_time': now, 'tt_status': 'closed',
                        'end_time': now})
            last_timeline = self.env['maintenance.request.timeline'].search(
                [('maintenance_request_id', '=', self.id), ('end_time', '=', False)], limit=1)
            if last_timeline:
                last_timeline.write({
                    'end_time': now,
                })
            else:
                self.env['maintenance.request.timeline'].create({
                    'maintenance_request_id': self.id,
                    'start_time': now,
                    'end_time': now,
                })

    @api.depends('job_order_ids')
    def _compute_job_order_count(self):
        for record in self:
            record.job_order_count = len(record.job_order_ids)

    def _get_duration(self, date_start, date_stop):
        if not date_start or not date_stop:
            return 0
        dt = date_stop - date_start
        return dt.seconds % (24 * 3600)

    @api.depends('tt_issuing_time', 'closing_outage_time')
    def _get_outage_duration(self):
        for record in self:
            record.outage_duration = record._get_duration(record.tt_issuing_time, record.closing_outage_time)
            hour = record.outage_duration // 3600
            record.outage_duration %= 3600
            duration_minutes = record.outage_duration // 60
            record.outage_duration %= 60

            hours = str(int(hour)) if hour else '00'
            minutes = str(int(duration_minutes)) if duration_minutes else '00'
            seconds = str(int(record.outage_duration)) if record.outage_duration else '00'
            hours_str = '0' + hours if len(hours) == 1 else hours
            minutes_str = '0' + minutes if len(minutes) == 1 else minutes
            seconds_str = '0' + seconds if len(seconds) == 1 else seconds
            record.outage_duration_str = hours_str + ':' + minutes_str + ':' + seconds_str

    @api.depends('starting_time', 'end_time', 'maintenance_type')
    def _get_duration_str(self):
        for record in self:
            if record.maintenance_type in ['corrective', 'preventive']:
                duration_seconds = 0
                for line in record.request_timeline_ids:
                    duration_seconds += record._get_duration(line.start_time, line.end_time)
            else:
                duration_seconds = record._get_duration(record.starting_time, record.end_time)
            hour = duration_seconds // 3600
            duration_seconds %= 3600
            duration_minutes = duration_seconds // 60
            duration_seconds %= 60
            hours = str(int(hour)) if hour else '00'
            minutes = str(int(duration_minutes)) if duration_minutes else '00'
            seconds = str(int(duration_seconds)) if duration_seconds else '00'
            hours_str = '0' + hours if len(hours) == 1 else hours
            minutes_str = '0' + minutes if len(minutes) == 1 else minutes
            seconds_str = '0' + seconds if len(seconds) == 1 else seconds
            record.duration_str = hours_str + ':' + minutes_str + ':' + seconds_str

    def action_view_job_order(self):
        return {
            'name': _('Job Orders'),
            'res_model': 'maintenance.job.order',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('ejaf_maintenance.maintenance_job_order_tree').id, 'tree'),
                (self.env.ref('ejaf_maintenance.maintenance_job_order_form_view').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'domain': [('maintenance_id', '=', self.id)],
        }

    def action_view_checklist(self):
        for record in self:
            ti_obj = self.env['technical.inspection']
            maintenance_inspection = ti_obj.sudo().search([('maintenance_id', '=', record.id)])
            return {
                "type": "ir.actions.act_window",
                "res_model": "technical.inspection",
                "views": [[self.env.ref('ejaf_maintenance.ti_form_view').id, "form"]],
                "res_id": maintenance_inspection[0].id if maintenance_inspection else False,
                'context': {'create': False},
            }

    def button_open_request_timeline(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "maintenance.request.timeline",
            "views": [[self.env.ref('ejaf_maintenance.maintenance_request_timeline_tree_view').id, "tree"]],
            "domain": [('id', 'in', self.request_timeline_ids.ids)],
        }

    def action_create_job_order(self):
        self.env['maintenance.job.order'].sudo().create({'maintenance_id': self.id,
                                                         'equipment_id': self.equipment_id.id,
                                                         })
        return self.action_view_job_order()
