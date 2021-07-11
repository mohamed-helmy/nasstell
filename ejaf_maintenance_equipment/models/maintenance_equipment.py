# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    category_type = fields.Selection([('hub', 'Hub'), ('mini_hub', 'Mini Hub'), ('normal', 'Normal')], default='normal',
                                     string='Severity Type')


class SiteSpmsActive(models.Model):
    _name = 'site.spms.active'
    _rec_name = 'name'
    _description = 'Site Spms Active'

    name = fields.Char(required=True)


class SiteZone(models.Model):
    _name = 'site.zone'
    _rec_name = 'name'
    _description = 'Site Zone'

    name = fields.Char(required=True)


class SiteSpmsPassive(models.Model):
    _name = 'site.spms.passive'
    _rec_name = 'name'
    _description = 'Site Spms Passive'

    name = fields.Char(required=True)


class Siterbss(models.Model):
    _name = 'site.rbss'
    _rec_name = 'name'
    _description = 'Site Rbss'

    name = fields.Char(required=True)
    value = fields.Integer()


class GuardInfo(models.Model):
    _name = 'guard.info'

    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    salary = fields.Float(string='Salary')
    currency_id = fields.Many2one('res.currency', string='Currency')


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    def _get_reservation_liters(self):
        reservation_liters = float(self.env['ir.config_parameter'].sudo().get_param('reservation_liters'))
        return reservation_liters

    site = fields.Char(string="Code", tracking=True)
    maintenance_team_id = fields.Many2one('maintenance.team', string='Maintenance Team', check_company=True,
                                          tracking=True)
    effected_sites_no = fields.Integer(string="no. Effected sites", compute='get_effected_sites_no', store=1,
                                       tracking=True)
    effected_sites_cell = fields.Char(string="no. of effected cells", tracking=True)
    bsc_name = fields.Char(string=" BSC name", tracking=True)
    tg_number = fields.Integer(string='TG No', tracking=True)
    no_for_ericsson = fields.Char(string="TG. No for Ericsson", tracking=True)
    bcf_no = fields.Char(string="BCF No.", tracking=True)
    region_id = fields.Many2one(comodel_name="region", string="Region", tracking=True)
    ne_impacted_id = fields.Many2one(comodel_name="ne.impacted", string="NE Impacted", tracking=True)
    ne_type_id = fields.Many2one(comodel_name="ne.type", string="NE Type", tracking=True)
    number_of_guards = fields.Integer(string='Number of Guard', tracking=True)
    assign_date = fields.Date('Onair Date', tracking=True)
    ph = fields.Char(string="", tracking=True)
    type_id_od_id = fields.Many2one(comodel_name="od.type", string="TYPE (ID/OD)", tracking=True)

    type_rt_gf_id = fields.Many2one(comodel_name="rt.type", string="TYPE (RT/GF)", tracking=True)
    commercial_generator_availability = fields.Selection(string="Commercial Generator Availability",
                                                         selection=[('yes', 'Yes'), ('no', 'No'),
                                                                    ('null', 'Null value')])
    # fuel_tank_capacity = fields.Float(string="Fuel Tank Capacity", tracking=True)
    fuel_tank_status = fields.Selection(string="Fuel Tank Status", selection=[('cow', 'Cow'), ('old', 'Old'),
                                                                              ('space', 'Space'), ], tracking=True)
    guard_ids = fields.One2many('guard.info', 'equipment_id', string='Guards')
    generator_qty = fields.Integer(string="Generator Qty", tracking=True)
    site_installed_id = fields.Many2one(comodel_name="res.partner", string="Site Installed by",
                                        domain=[("is_company", "=", True)], tracking=True)
    maintenance_by_id = fields.Many2one(comodel_name="res.partner", string="Maintenance BY",
                                        domain=[("is_company", "=", True)], tracking=True)
    is_commercial_power = fields.Boolean(string="Commercial Power", tracking=True)
    commercial_date = fields.Date(string="Date of commercial", tracking=True)
    power_phases = fields.Selection(string="Power is single or 3 phases", selection=[('single', 'Single'),
                                                                                     ('3_phases', '3 Phases')],
                                    tracking=True)
    commercial_generator_date = fields.Date(string="Connected commercial generator date", tracking=True)
    generator_available_by_load = fields.Integer(string="If Commercial Generator Available Load by Amp", tracking=True)
    distance_commercial_generator = fields.Float(string="Distance from Commercial Generator to the site/m",
                                                 tracking=True)
    korek_transformer = fields.Float(string="Korek CP Transformer KVA", tracking=True)
    electric_contract_id = fields.Char(string='Electric Contract ID')
    payment = fields.Char(string='Payment')
    ventilation = fields.Selection(string="Ventilation", selection=[('no', 'No'), ('yes', 'Yes'), ('a_n', 'N/A')],
                                   tracking=True)
    generator_ids = fields.One2many(comodel_name="site.generator", inverse_name="site_id")
    fuel_ids = fields.One2many(comodel_name="fuel.planning", inverse_name="site_id")
    air_condition_ids = fields.One2many(comodel_name="site.air.condition", inverse_name="site_id")
    air_condition_qty = fields.Float(string="Qty", tracking=True)
    air_condition_uom_id = fields.Many2one(comodel_name='uom.uom', string='Unit of Measure', tracking=True)
    rbs_qty = fields.Integer(string="RBS QTY", tracking=True)
    site_rbss_id = fields.Many2one(comodel_name="site.rbss", string="RBSs", tracking=True)
    batt_produced_date = fields.Date(string="Batt/Produced date", tracking=True)
    batt_installed_date = fields.Date(string="Batt/installed date", tracking=True)

    batte_soh = fields.Char(string="Batt/ SOH", tracking=True)
    batt_qty = fields.Float(string="Batt/ QTY", tracking=True)
    battery_brand = fields.Char(string="Ah/Battery Brand", tracking=True)

    rectifiers_qty = fields.Integer(string="Rectifiers  Qty", tracking=True)
    dc_system_line_ids = fields.One2many(comodel_name="dc.system.line", inverse_name="maintenance_equipment_id",
                                         string="", required=False, )
    fm_200_availability = fields.Char(string="FM 200 Availability", tracking=True)
    fm_200_availability_sim = fields.Char(string="If FM200 Available SIM Card NO.", tracking=True)
    installed_fm_date = fields.Float(string="installed FM200 date", tracking=True)
    fm_cylinder_wight = fields.Float(string="FM200 Cylinder wieght (Gas Qty by Kg)", tracking=True)

    grouping_system_korek = fields.Selection(string="Grounding system according to Korek specs or Not",
                                             selection=[('yes', 'Yes'), ('no', 'No'), ('share', 'Share'), ],
                                             tracking=True)
    grouping_date_enhancement = fields.Integer(string="Grounding Date enhancement", tracking=True)
    grouping_installed_id = fields.Many2one(comodel_name="res.partner", string="Installed by",
                                            domain=[("is_company", "=", True)], tracking=True)
    rocky_normal_soil = fields.Selection(string="Rocky/Normal soil", selection=[('rocky', 'Rocky'), ('soil', 'Soil')],
                                         tracking=True)

    exteral_alarm_availability = fields.Char(string="External Alarm availability", tracking=True)
    connected = fields.Char(string="Connected", tracking=True)
    configured = fields.Char(string="Configured", tracking=True)
    urban_rural = fields.Selection(string="Urban or Rural", selection=[('urban', 'Urban'), ('rular', 'Rural')],
                                   tracking=True)
    numbers_of_alarms = fields.Integer(string="numbers of Alarms", required=False, tracking=True)

    aviation_availability = fields.Char(string="Aviation Availability", tracking=True)
    aviation_status = fields.Char(string="Aviation  Status", tracking=True)
    guard = fields.Selection(string="Guard (Yes or No)", selection=[('yes', 'Yes'), ('no', 'No')], tracking=True)

    power_note = fields.Text(tracking=True)
    supply_power = fields.Boolean(tracking=True)
    ac_belong_korek = fields.Char(string="A/C belong Korek", tracking=True)

    ac_belong_nawroz = fields.Char(string="AC power Nawroz", tracking=True)
    supply_power_dil = fields.Char(string="supply power to Dil", tracking=True)
    iraq_cell = fields.Char(string="IraqCell DWDM/Load", tracking=True)
    ats_type = fields.Selection(string="ATS type", selection=[('abb', 'ABB'), ('cow', 'COW'), ('local', 'Local')
        , ('sch', 'SCH')], tracking=True)
    sites_location = fields.Char(string="Sites Location &amp; Dist. From Duhok center  (Km)", tracking=True)

    flm_id = fields.Many2one(comodel_name="res.partner", string="FLM", domain=[("is_company", "=", True)],
                             tracking=True)
    spms_active_id = fields.Many2one(comodel_name="site.spms.active", string="SPMS Active", tracking=True)
    spms_passive_id = fields.Many2one(comodel_name="site.spms.passive", string="SPMS Passive", tracking=True)
    fuel_id = fields.Many2one(comodel_name="res.partner", string="Fuel", domain=[("is_company", "=", True)],
                              tracking=True)
    company_id = fields.Many2one(comodel_name='res.company', string="Managed by",
                                 default=lambda self: self.env.company, tracking=True)
    status = fields.Selection(string="Status", selection=[('on', 'On'), ('off', 'Off'), ], tracking=True)
    zone_id = fields.Many2one(comodel_name="site.zone", string="Zone", tracking=True)
    category_type = fields.Selection([('hub', 'Hub'), ('mini_hub', 'Mini Hub'), ('normal', 'Normal')],
                                     string='Severity Type', related="category_id.category_type", store=False,
                                     tracking=True)
    parent_id = fields.Many2one(comodel_name="maintenance.equipment", tracking=True)
    child_ids = fields.Many2many('maintenance.equipment', 'maintenance_equipment_rel', 'equipment_id', 'parent_id',
                                 string='Child Sites')
    # child_ids = fields.One2many('maintenance.equipment', 'parent_id', string='Child Sites')
    planning_ids = fields.One2many(comodel_name="site.planning", inverse_name="site_id")

    last_pred_maintenance_request_date = fields.Date(compute='get_last_pred_maintenance_request_date', tracking=True)

    # fields for predictive plan for generator
    ###################################################################
    planned_generator_ids = fields.Many2many("site.generator", ondelete="cascade", tracking=True)

    planning_lines_ids = fields.One2many('generator.planning.line', 'site_id', string='Generator Planning Lines')
    generator_planning_ids = fields.One2many(comodel_name="generator.planning", inverse_name="site_id",
                                             string='Generator Plannings')
    recurring_rule_type = fields.Selection([('daily', 'Days'), ('weekly', 'Weeks'),
                                            ('monthly', 'Months'), ('yearly', 'Years'), ],
                                           string='Recurrence', required=True,
                                           help="repeat at specified interval",
                                           default='monthly', tracking=True)
    recurring_interval = fields.Integer(string="Period", help="Repeat every (Days/Week/Month/Year)",
                                        required=True, default=1, tracking=True)
    recurring_rule_boundary = fields.Selection([
        ('limited', 'Number of repetitions'),
        ('end_date', 'End date')
    ], string='Recurrence Termination', default='limited', required=1, tracking=True)
    recurring_rule_count = fields.Integer(string="End After", default=1, tracking=True)
    date_start = fields.Date(string='Start Date', default=fields.Date.today, required=1, tracking=True)
    date_end = fields.Date(string='End Date', tracking=True)

    tank_size = fields.Float(string=' Fuel Tank Capacity/Lit', tracking=True)
    site_type_id = fields.Many2one('site.type', string='Site Type', tracking=True)
    group = fields.Selection([('data_center', 'Data Center'), ('major', 'Major'), ('normal', 'Normal')], string='Group',
                             default='data_center', tracking=True)
    reservation_liters = fields.Float(string='Reservation Liters', tracking=True, default=_get_reservation_liters)
    owner_name = fields.Char(string='Owner Name', tracking=True)
    contract_id = fields.Char(string='Contract ID', tracking=True)
    payment_type = fields.Selection([('month', 'Month'), ('year', 'Year')], string='Payment Type', default='month',
                                    tracking=True)
    payment_amount = fields.Float(string='Payment Amount', tracking=True)
    id_of_payment = fields.Char(string='ID of Payment', tracking=True)

    du_type_2g = fields.Char(string="DU Type For 2G")
    du_type_2g_qty = fields.Float(string="DU type For 2G (Qty)")
    du_type_3g = fields.Char(string="DU Type For 3G")
    du_type_3g_qty = fields.Float(string="DU type For 3G (Qty)")
    abis_solt_type = fields.Selection(string="ABIS Slot type (TCU or R6K)",
                                      selection=[('null', 'Null Value'), ('tcu', 'TCU'), ('r6k', 'R6K')])
    ru_type_sector = fields.Char(string="RU type per sector")
    ru_type_sector_hight = fields.Float(string="RU type per sector (Hight)")
    antenna_type_sector = fields.Char(string="Antenna type per sector")
    antenna_type_sector_hight = fields.Float(string="Antenna type per sector (Hight)")
    azimuth_for_each = fields.Char(string="Azimuth for each")
    no_of_psu = fields.Integer(string="No. of PSU")
    psu_type = fields.Char(string="PSU Type")
    no_of_pdu = fields.Char(string="No. of PDU")
    pdu_type = fields.Char(string="PDU Type")
    national_grid_power = fields.Char(string="National Grid POWER")
    tower_type_id = fields.Many2one(comodel_name="tower.type", string="Tower Type (Mast , LS, COW , RT , GF)")
    tower_hight = fields.Float(string="Tower Height. (m)")
    building_hight = fields.Float(string=" Building Height. (m)")
    tower_stamp = fields.Char(string="Tower Stamp", required=False, )
    shelter_availability = fields.Char(string="Shelter Availability(YES||NO)")
    shelter_dimension = fields.Char(string="Shelter Dimension(W,L,H)")
    site_dimension = fields.Char(string="Site Dimension (W,L)m")
    site_cascaded = fields.Char(string="Sites Cascaded (Traffic dependency)")
    fuel_tank_type_id = fields.Many2one(comodel_name="fuel.tank.type", string="Fuel Tank Type")
    ats_availability = fields.Char(string="ATS availability", required=False, )
    ats_stand_availability = fields.Char(string="ATS stand Availability", required=False, )
    ats_model_id = fields.Many2one(comodel_name="ats.model", string="ATS model", required=False, )
    ats_according_specs = fields.Char(string="ATS According Specs", required=False, )
    ats_contractors = fields.Char(string="ATS Contractors", required=False, )
    mde_availability = fields.Char(string="MDB Availability", required=False, )
    mde_stand_availability = fields.Char(string="MDB Stand Availability", required=False, )
    mde_according_to_specs = fields.Char(string="MDB According To Specs", required=False, )
    cp_board_availability = fields.Char(string="CP Board Availability", required=False, )
    cp_board_according_specs = fields.Char(string="CP Board According Specs", required=False, )
    kwh_meter = fields.Char(string="KWh Meter S/Nr", required=False, )
    cp_account_nr = fields.Char(string="CP Account Nr", required=False, )
    cg_connected = fields.Char(string="CG Connected or Not", required=False, )
    ext_ats_availability = fields.Char(string="Ext.ATS availability", required=False, )
    cg_owner_name = fields.Char(string="CG Owner Name", required=False, )
    cg_operator = fields.Char(string="CG Operator", required=False, )
    cg_accountant_name = fields.Char(string="CG Accountant Name", required=False, )
    cg_connected_mcb = fields.Char(string="CG Connected MCB", required=False, )
    cg_payment_a = fields.Char(string="CG payment [A]", required=False, )
    accu_board_availability = fields.Char(string="ACCU Board Availability", required=False, )
    rbs_model_id = fields.Many2one(comodel_name="rbs.model", string="RBS Model", required=False, )
    battery_manufacturing_date = fields.Date(string="Battery Manufacturing Date", required=False, )
    battery_manufacturer_id = fields.Many2one(comodel_name="battery.manufacturer", string="Battery Manufacturer",
                                              required=False, )
    battery_model_id = fields.Many2one(comodel_name="battery.model", string="Battery Model", required=False, )
    fiber_connection_id = fields.Many2one(comodel_name="fiber.connection", string="Fiber Connection", required=False, )
    mw_link_type = fields.Selection(string="MW link Type (Ericsson/NOKIA)",
                                    selection=[('null', 'Null value'), ('nokia', 'Nokia'),
                                               ('ericsson', 'Ericsson'), ], required=False, )
    trm_cabinet = fields.Char(string="TRM Cabinet", required=False, )
    mw_antenna_size = fields.Float(string="MW Antenna size", required=False, )
    radio_type_id = fields.Many2one(comodel_name="radio.type", string="Radio Type", required=False, )
    mmu_type_id = fields.Many2one(comodel_name="mmu.type", string="MMU Type", required=False, )
    amm_type_id = fields.Many2one(comodel_name="amm.type", string="AMM  Type", required=False, )
    grounding_system_according_korek_specs = fields.Char(string="Grounding system According To Korek Specs or Not",
                                                         required=False, )
    number_of_delta = fields.Integer(string="Number of Delta", required=False, )
    busbar_qty = fields.Float(string="Busbar Qty", required=False, )
    lightning_rod_availability = fields.Char(string="Lightning Rod availability", required=False, )
    rbs_sunshade = fields.Char(string="RBS Sunshade", tracking=True)
    rbs_according_specs = fields.Char(string="RBS according to specs", tracking=True)
    generator_sunshade = fields.Char(string="Generator Sunshade", tracking=True)
    generator_sunshade_according_specs = fields.Char(string="Generator Sunshade According TO Specs", tracking=True)
    antenna_type_id = fields.Many2one(comodel_name="antenna.type", string="Antenna Type", tracking=True)
    l_type_id = fields.Many2one(comodel_name="l.type", string="L-Type", tracking=True)
    antenna_support_qty = fields.Float(string="Antenna Support qty", tracking=True, )
    cctv = fields.Char(string="CCTV", tracking=True, )
    no_camera = fields.Integer(string="NO.Camera", tracking=True, )
    dvr_type_id = fields.Many2one(comodel_name="dvr.type", string="DVR Type", tracking=True)
    gen_set_manufacturer_id = fields.Many2one(comodel_name="gen.set.manufacturer", string="Gen-Set Manufacturer",
                                              required=False, )
    tower_topology_id = fields.Many2one(comodel_name="tower.topology",
                                        string="Tower Topology (RT/GF)", required=False, )
    clu_status_id = fields.Many2one(comodel_name="clu.status",
                                    string="CLU Status", required=False, )
    site_location_id = fields.Many2one('stock.location', string='Site Location')

    @api.model
    def create(self, vals):
        stock_location = self.env['stock.location'].sudo().create({'name': vals['name'],
                                                                   'usage': 'internal',
                                                                   'company_id': self.env.company.id})
        vals['site_location_id'] = stock_location.id
        return super(MaintenanceEquipment, self).create(vals)

    @api.constrains('fuel_ids')
    def set_next_visit(self):
        for record in self:
            for plan in record.fuel_ids:
                for line in plan.planning_lines_ids:
                    if line.maintenance_request_id and line.maintenance_request_id.starting_time_date and line.maintenance_request_id.next_visit_plan:
                        self.env['fuel.planning.line'].sudo().create({'site_id': line.site_id.id,
                                                                      'plan_id': plan.id,
                                                                      'date': line.maintenance_request_id.next_visit_plan})

                #

    @api.constrains('recurring_rule_count', 'recurring_interval', 'planned_generator_ids')
    def check_recurring(self):
        for rec in self:
            if rec.recurring_rule_count <= 0 and rec.planned_generator_ids:
                raise ValidationError(_('Number of repetitions should be greater than 0.'))
            if rec.recurring_interval <= 0 and rec.planned_generator_ids:
                raise ValidationError(_('Period should be greater than 0.'))

    @api.onchange('planned_generator_ids')
    def onchange_generator_id(self):
        for line in self.planning_lines_ids:
            if line.maintenance_request_id:
                raise ValidationError(
                    _('You cannot change a generator which has a maintenance request.'))

    @api.model
    def _get_next_date(self, interval_type, interval, current_date):
        recurring_invoice_day = current_date.day
        periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
        interval_type = periods[interval_type]
        recurring_next_date = fields.Date.from_string(current_date) + relativedelta(**{interval_type: interval})
        if interval_type == 'months':
            last_day_of_month = recurring_next_date + relativedelta(day=31)
            if last_day_of_month.day >= recurring_invoice_day:
                # In cases where the next month does not have same day as of previous recurrent date, we set the last date of next month
                # Example: current_date is 31st January then next date will be 28/29th February
                return recurring_next_date.replace(day=recurring_invoice_day)
            # In cases where the date on the last day of a particular month then it should stick to last day for all recurrent months
            # Example: 31st January, 28th February, 31st March, 30 April and so on.
            return last_day_of_month
        # Return the next day after adding interval
        return recurring_next_date

    @api.onchange('date_start', 'date_end', 'recurring_rule_type', 'recurring_rule_count', 'recurring_rule_boundary',
                  'recurring_interval', 'planned_generator_ids')
    def onchange_date_start(self):
        planning_lines_without_maintenance_requests = self.planning_lines_ids.filtered(
            lambda x: not x.maintenance_request_id)
        self.planning_lines_ids -= planning_lines_without_maintenance_requests
        vals_list = []
        if self.date_start and self.recurring_rule_boundary:
            if self.recurring_rule_boundary == 'limited' and self.recurring_rule_count and self.recurring_interval:
                last_planned_date = self.date_start
                for i in range(self.recurring_rule_count):
                    if i == 0:
                        vals = {
                            'plan_week': self.get_week_number(last_planned_date),
                            'date': last_planned_date,
                        }
                    else:
                        last_planned_date = self._get_next_date(self.recurring_rule_type, self.recurring_interval,
                                                                last_planned_date)
                        vals = {
                            'plan_week': self.get_week_number(last_planned_date),
                            'date': last_planned_date,
                        }
                    vals_list.append((0, 0, vals))
            if self.recurring_rule_boundary == 'end_date' and self.date_end and self.recurring_interval:
                last_planned_date = self.date_start

                i = 0
                while self.date_end > last_planned_date:
                    if i == 0:
                        vals = {
                            'plan_week': self.get_week_number(last_planned_date),
                            'date': last_planned_date,
                        }
                    else:
                        last_planned_date = self._get_next_date(self.recurring_rule_type, self.recurring_interval,
                                                                last_planned_date)
                        last_planned_date = last_planned_date if last_planned_date < self.date_end else self.date_end
                        vals = {
                            'plan_week': self.get_week_number(last_planned_date),
                            'date': last_planned_date,
                        }
                    # vals['maintenance_team_id'] = self.maintenance_team_id.id
                    vals_list.append((0, 0, vals))
                    i += 1

        if vals_list:
            self.planning_lines_ids = vals_list

    def get_week_number(self, date):
        day_weeks = {
            '01': '1',
            '02': '1',
            '03': '1',
            '04': '1',
            '05': '1',
            '06': '1',
            '07': '1',
            '08': '2',
            '09': '2',
            '10': '2',
            '11': '2',
            '12': '2',
            '13': '2',
            '14': '2',
            '15': '3',
            '16': '3',
            '17': '3',
            '18': '3',
            '19': '3',
            '20': '3',
            '21': '3',
            '22': '4',
            '23': '4',
            '24': '4',
            '25': '4',
            '26': '4',
            '27': '4',
            '28': '4',
            '29': '5',
            '30': '5',
            '31': '5',
        }
        day = date.strftime("%d")
        return day_weeks[day]

    ###################################################################

    @api.constrains('category_id.category_type', 'child_ids', 'category_id')
    def _check_child_ids(self):
        for record in self:
            if record.category_id and not record.parent_id and not record.child_ids and not record.category_id.category_type:
                raise ValidationError(_('You cannot save without related sites.'))

    def get_last_pred_maintenance_request_date(self):
        for rec in self:
            r = self.env['maintenance.request'].search(
                [('equipment_id', '=', rec.id), ('maintenance_type', '=', 'preventive')],
                order='request_date desc', limit=1)
            if r and r.request_date:
                rec.last_pred_maintenance_request_date = r.request_date
            else:
                rec.last_pred_maintenance_request_date = False

    @api.depends('child_ids')
    def get_effected_sites_no(self):
        for rec in self:
            rec.effected_sites_no = len(rec.child_ids)

    def write(self, vals):
        res = super(MaintenanceEquipment, self).write(vals)
        if vals.get('parent_id', False):
            for rec in self:
                if rec.parent_id and rec not in rec.parent_id.child_ids:
                    rec.parent_id.child_ids = [(4, rec.id)]
        return res
