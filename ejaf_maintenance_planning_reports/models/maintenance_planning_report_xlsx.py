# -*- coding: utf-8 -*-

from odoo import models
from datetime import date
import calendar
import io
import base64

MONTHS = [('1', "January"),
          ('2', "February"),
          ('3', "March"),
          ('4', "April"),
          ('5', "May"),
          ('6', "June"),
          ('7', "July"),
          ('8', "August"),
          ('9', "September"),
          ('10', "October"),
          ('11', "November"),
          ('12', "December")]


class MaintenancePlanningReportXlsx(models.AbstractModel):
    _name = 'report.ejaf_maintenance_planning_reports.maintenance_reports'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard_data):
        if data['site_plan']:
            worksheet = workbook.add_worksheet("Site Plan Report")
            f1 = workbook.add_format(
                {'bold': True, 'font_color': '#000000', 'align': 'center', 'font_size': 16, 'bg_color': '#6c6fa1'})

            f2 = workbook.add_format(
                {'bold': False, 'font_color': '#ffffff', 'align': 'center', 'bg_color': '#4f33ff', 'border': True})
            f3 = workbook.add_format(
                {'bold': True, 'font_color': '#000000', 'align': 'center', 'border': True})
            year = int(data['year'])
            month = int(data['month'])
            month_name = dict(MONTHS)[data['month']]
            worksheet.merge_range('A1:C2', 'PM Plan Of ' + str(month_name), f1)
            start_date = date(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end_date = date(year, month, last_day)
            site_planning_lines = self.env['site.planning.line'].sudo().search(
                [('date', '>=', start_date), ('date', '<=', end_date)])
            maintenance_users = []
            for site_plan_line in site_planning_lines:
                if (
                        site_plan_line.maintenance_request_id and site_plan_line.maintenance_request_id.user_id and site_plan_line.maintenance_request_id.user_id.id not in maintenance_users):
                    maintenance_users.append(site_plan_line.maintenance_request_id.user_id.id)
                elif (
                        site_plan_line.maintenance_team_id and site_plan_line.maintenance_team_id.team_leader_id and site_plan_line.maintenance_team_id.team_leader_id.id not in maintenance_users):
                    maintenance_users.append(site_plan_line.maintenance_team_id.team_leader_id.id)
            row = 3
            col = 1
            if maintenance_users:
                week1_sites = site_planning_lines.filtered(
                    lambda ss: ss.plan_week == '1')
                week2_sites = site_planning_lines.filtered(
                    lambda ss: ss.plan_week == '2')
                week3_sites = site_planning_lines.filtered(
                    lambda ss: ss.plan_week == '3')
                week4_sites = site_planning_lines.filtered(
                    lambda ss: ss.plan_week == '4')
                max_week_sites = max(len(week1_sites), len(week2_sites), len(week3_sites), len(week4_sites))
                for week in range(1, 5):
                    week_achieved = 0
                    worksheet.merge_range(row, col, row, col + max_week_sites, 'Week' + str(week), f2)
                    worksheet.merge_range(row, 0, row + 2, 0, 'Plan', f2)
                    worksheet.write(row + 3, 0, 'Achieve', f2)
                    worksheet.set_column(row + 3, 0, 20)
                    new_col = 1
                    total_week_sites = len(site_planning_lines.filtered(
                        lambda ss: ss.plan_week == str(week)))
                    maintenance_sites = 0
                    remain_sites = max_week_sites
                    worksheet.write(row + 1, max_week_sites + 1, 'Total', f3)
                    worksheet.set_column(row + 1, max_week_sites + 1, 20)
                    site_index = 0
                    week_sites = []
                    non_user_sites = []
                    for user in maintenance_users:
                        user_obj = self.env['res.users'].sudo().browse(user)
                        user_sites = []
                        for plan_line in site_planning_lines.filtered(lambda ss: ss.plan_week == str(week)):
                            if plan_line.maintenance_request_id and plan_line.maintenance_request_id.user_id and plan_line.maintenance_request_id.user_id.id == user and plan_line.id not in user_sites and plan_line.id not in week_sites:
                                user_sites.append(plan_line.id)
                                week_sites.append(plan_line.id)
                            if not plan_line.maintenance_request_id and plan_line.id not in non_user_sites and plan_line.id not in week_sites:
                                non_user_sites.append(plan_line.id)
                                week_sites.append(plan_line.id)
                            # elif plan_line.maintenance_team_id and plan_line.maintenance_team_id.team_leader_id and plan_line.maintenance_team_id.team_leader_id.id == user and plan_line.id not in user_sites and plan_line.id not in week_sites:
                            #     user_sites.append(plan_line.id)
                            #     week_sites.append(plan_line.id)
                        if user_sites:
                            if len(user_sites) > 1:
                                worksheet.merge_range(row + 1, new_col, row + 1, new_col + len(user_sites) - 1,
                                                      user_obj.name,
                                                      f3)
                            else:
                                worksheet.write(row + 1, new_col, user_obj.name, f3)
                            for site in user_sites:
                                site_obj = self.env['site.planning.line'].sudo().browse(site)
                                worksheet.write(row + 2, col + site_index, site_obj.site_id.name, f3)
                                worksheet.set_column(row + 2, col + site_index, 20)
                                if site_obj.maintenance_request_id.stage_id.done:
                                    week_achieved += 1
                                    worksheet.write(row + 3, col + site_index, 'Ok', f3)
                                    worksheet.set_column(row + 3, col + site_index, 20)
                                else:
                                    worksheet.write(row + 3, col + site_index, '', f3)
                                    worksheet.set_column(row + 3, col + site_index, 20)
                                site_index += 1
                        if len(user_sites) > 1:
                            new_col += new_col + len(user_sites) - 1
                        else:
                            new_col += len(user_sites)
                        remain_sites -= len(user_sites)
                        maintenance_sites += len(user_sites)
                    non_maintenance_sites = (total_week_sites - maintenance_sites)
                    remain_sites -= non_maintenance_sites
                    for item in non_user_sites:
                        non_site = self.env['site.planning.line'].sudo().browse(item)
                        worksheet.write(row + 1, new_col,
                                        str(non_site.maintenance_team_id.name) if non_site.maintenance_team_id and non_site.maintenance_team_id.name else '',
                                        f3)
                        worksheet.write(row + 2, new_col, str(non_site.site_id.name), f3)
                        worksheet.write(row + 3, new_col, '', f3)
                        new_col += 1
                    for item in range(0, remain_sites):
                        worksheet.write(row + 1, new_col, '', f3)
                        worksheet.write(row + 2, new_col, '', f3)
                        worksheet.write(row + 3, new_col, '', f3)
                        new_col += 1
                    worksheet.write(row + 3, max_week_sites + 1, week_achieved, f3)
                    worksheet.write(row + 2, col + max_week_sites, str(total_week_sites), f3)
                    worksheet.set_column(row + 2, col + max_week_sites, 20)
                    row += 4
        else:
            worksheet = workbook.add_worksheet("Maintenance Planning Report")
            f1 = workbook.add_format(
                {'bold': True, 'font_color': '#000000', 'align': 'center', 'font_size': 16})
            f11 = workbook.add_format(
                {'bold': True, 'font_color': '#000000', 'align': 'center', 'font_size': 16, 'bg_color': '#ff33f0 ',
                 'border': True})
            f2 = workbook.add_format(
                {'bold': False, 'font_color': '#ffffff', 'align': 'center', 'bg_color': '#4f33ff', 'border': True})
            f3 = workbook.add_format(
                {'bold': True, 'font_color': '#000000', 'align': 'center', 'border': True})
            f4 = workbook.add_format(
                {'bold': False, 'font_color': '#000000', 'align': 'center', 'border': True})
            buf_image = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
            image_width = 340.0
            image_height = 140.0

            cell_width = 64.0
            cell_height = 20.0

            x_scale = cell_width / image_width
            y_scale = cell_height / image_height

            worksheet.insert_image('A1', "any_name.png",
                                   {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
            year = int(data['year'])

            if data['planning_type'] == 'summary':
                worksheet.merge_range('A11:F12', 'Summary Of PM Plan  ' + str(year), f1)
                total_planned = 0
                total_achieved = 0
                row = 13
                for month in range(1, 13):
                    month_name = dict(MONTHS)[str(month)]
                    start_date = date(year, month, 1)
                    last_day = calendar.monthrange(year, month)[1]
                    end_date = date(year, month, last_day)
                    site_planning_lines = self.env['site.planning.line'].sudo().search(
                        [('date', '>=', start_date), ('date', '<=', end_date)])
                    no_planned = len(site_planning_lines)
                    total_planned += no_planned
                    no_achieved = len(site_planning_lines.filtered(lambda ll: ll.achieved == 'OK'))
                    total_achieved += no_achieved
                    worksheet.merge_range(row, 0, row + 1, 2, month_name + ' Summary', f11)
                    worksheet.write(row, 3, 'Plan', f2)
                    worksheet.write(row + 1, 3, 'Achieve', f2)
                    worksheet.write(row, 4, str(no_planned), f2)
                    worksheet.write(row + 1, 4, str(no_achieved), f2)
                    row += 2
                worksheet.merge_range(18, 8, 19, 9, 'Total', f11)
                worksheet.write(18, 10, 'Plan', f2)
                worksheet.write(19, 10, 'Achieve', f2)
                worksheet.write(18, 11, str(total_planned), f2)
                worksheet.write(19, 11, str(total_achieved), f2)
            else:
                month = int(data['month'])
                month_name = dict(MONTHS)[data['month']]
                worksheet.merge_range('A11:F12', 'PM Plan Of ' + str(month_name), f1)
                start_date = date(year, month, 1)
                no_planned = 0
                no_achieved = 0
                last_day = calendar.monthrange(year, month)[1]
                end_date = date(year, month, last_day)
                site_planning_lines = self.env['site.planning.line'].sudo().search(
                    [('date', '>=', start_date), ('date', '<=', end_date)])
                maintenance_teams = []
                for site_plan in site_planning_lines:
                    if site_plan.maintenance_team_id.id not in maintenance_teams:
                        maintenance_teams.append(site_plan.maintenance_team_id.id)
                if maintenance_teams:
                    row = 13
                    col = 1
                    for week in range(1, 5):
                        sites = site_planning_lines.filtered(
                            lambda ss: ss.plan_week == str(week))
                        no_planned += len(sites)
                        if sites:
                            worksheet.merge_range(row, col, row, col + len(sites), 'Week' + str(week), f2)
                        else:
                            worksheet.merge_range(row, col, row, col + len(maintenance_teams), 'Week' + str(week), f2)
                        worksheet.merge_range(row, 0, row + 2, 0, 'Plan', f2)
                        team_index = 0
                        week_sites = False
                        team_row = 0
                        no_site_ok = 0
                        for team in maintenance_teams:
                            team_obj = self.env['maintenance.team'].sudo().browse(team)
                            row += 1
                            team_row = row
                            week_sites = site_planning_lines.filtered(
                                lambda ss: ss.maintenance_team_id.id == team and ss.plan_week == str(week))
                            if week_sites and len(week_sites) > 1:
                                worksheet.merge_range(row, col + team_index, row, col + len(week_sites) - 1,
                                                      str(team_obj.name),
                                                      f3)
                            else:
                                worksheet.write(row, col + team_index, str(team_obj.name), f3)
                            site_index = 0
                            no_site_ok = 0
                            row += 1
                            if week_sites:
                                for site in week_sites:
                                    worksheet.write(row, col + site_index, str(site.site_id.name), f4)
                                    if site.achieved == 'OK':
                                        no_site_ok += 1
                                        worksheet.merge_range(row + 1, col + site_index, row + 2, col + site_index,
                                                              str(site.achieved),
                                                              f4)
                                    else:
                                        worksheet.merge_range(row + 1, col + site_index, row + 2, col + site_index,
                                                              '',
                                                              f4)
                                    site_index += 1
                            if not week_sites:
                                worksheet.merge_range(row + 1, col + team_index, row + 2, col + team_index,
                                                      '',
                                                      f4)
                            team_index += 1
                            row += 1
                            if week_sites:
                                worksheet.write(team_row + 1, col + team_index + len(week_sites) - 1, str(site_index),
                                                f3)
                            else:
                                worksheet.write(team_row + 1, col + team_index, str(site_index), f3)
                        no_achieved += no_site_ok
                        if week_sites:
                            worksheet.write(team_row, col + team_index + len(week_sites) - 1, 'Total', f3)
                            worksheet.merge_range(row, col + team_index + len(week_sites) - 1, row + 1,
                                                  col + team_index + len(week_sites) - 1, str(no_site_ok), f3)
                        else:
                            buf_image = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
                            image_width = 340.0
                            image_height = 140.0

                            cell_width = 64.0
                            cell_height = 20.0

                            x_scale = cell_width / image_width
                            y_scale = cell_height / image_height

                            worksheet.insert_image('A1', "any_name.png",
                                                   {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
                            year = int(data['year'])
                            if data['planning_type'] == 'summary':
                                worksheet.merge_range('A11:F12', 'Summary Of PM Plan  ' + str(year), f1)
                                total_planned = 0
                                total_achieved = 0
                                row = 13
                                for month in range(1, 13):
                                    month_name = dict(MONTHS)[str(month)]
                                    start_date = date(year, month, 1)
                                    last_day = calendar.monthrange(year, month)[1]
                                    end_date = date(year, month, last_day)
                                    site_planning_lines = self.env['site.planning.line'].sudo().search(
                                        [('date', '>=', start_date), ('date', '<=', end_date)])
                                    no_planned = len(site_planning_lines)
                                    total_planned += no_planned
                                    no_achieved = len(site_planning_lines.filtered(lambda ll: ll.achieved == 'OK'))
                                    total_achieved += no_achieved
                                    worksheet.merge_range(row, 0, row + 1, 2, month_name + ' Summary', f11)
                                    worksheet.write(row, 3, 'Plan', f2)
                                    worksheet.write(row + 1, 3, 'Achieve', f2)
                                    worksheet.write(row, 4, str(no_planned), f2)
                                    worksheet.write(row + 1, 4, str(no_achieved), f2)
                                    row += 2
                                worksheet.merge_range(18, 8, 19, 9, 'Total', f11)
                                worksheet.write(18, 10, 'Plan', f2)
                                worksheet.write(19, 10, 'Achieve', f2)
                                worksheet.write(18, 11, str(total_planned), f2)
                                worksheet.write(19, 11, str(total_achieved), f2)
                            else:
                                month = int(data['month'])
                                month_name = dict(MONTHS)[data['month']]
                                worksheet.merge_range('A11:F12', 'PM Plan Of ' + str(month_name), f1)
                                start_date = date(year, month, 1)
                                no_planned = 0
                                no_achieved = 0
                                last_day = calendar.monthrange(year, month)[1]
                                end_date = date(year, month, last_day)
                                site_planning_lines = self.env['site.planning.line'].sudo().search(
                                    [('date', '>=', start_date), ('date', '<=', end_date)])
                                maintenance_teams = []
                                for site_plan in site_planning_lines:
                                    if site_plan.maintenance_team_id.id not in maintenance_teams:
                                        maintenance_teams.append(site_plan.maintenance_team_id.id)
                                if maintenance_teams:
                                    row = 13
                                    col = 1
                                    for week in range(1, 5):
                                        sites = site_planning_lines.filtered(
                                            lambda ss: ss.plan_week == str(week))
                                        no_planned += len(sites)
                                        if sites:
                                            worksheet.merge_range(row, col, row, col + len(sites), 'Week' + str(week),
                                                                  f2)
                                        else:
                                            worksheet.merge_range(row, col, row, col + len(maintenance_teams),
                                                                  'Week' + str(week), f2)
                                        worksheet.merge_range(row, 0, row + 2, 0, 'Plan', f2)
                                        team_index = 0
                                        week_sites = False
                                        team_row = 0
                                        no_site_ok = 0
                                        for team in maintenance_teams:
                                            team_obj = self.env['maintenance.team'].sudo().browse(team)
                                            row += 1
                                            team_row = row
                                            week_sites = site_planning_lines.filtered(
                                                lambda ss: ss.maintenance_team_id.id == team and ss.plan_week == str(
                                                    week))
                                            if week_sites and len(week_sites) > 1:
                                                worksheet.merge_range(row, col + team_index, row,
                                                                      col + len(week_sites) - 1,
                                                                      str(team_obj.name),
                                                                      f3)
                                            else:
                                                worksheet.write(row, col + team_index, str(team_obj.name), f3)
                                            site_index = 0
                                            no_site_ok = 0
                                            row += 1
                                            if week_sites:
                                                for site in week_sites:
                                                    worksheet.write(row, col + site_index, str(site.site_id.name), f4)
                                                    if site.achieved == 'OK':
                                                        no_site_ok += 1
                                                        worksheet.merge_range(row + 1, col + site_index, row + 2,
                                                                              col + site_index,
                                                                              str(site.achieved),
                                                                              f4)
                                                    else:
                                                        worksheet.merge_range(row + 1, col + site_index, row + 2,
                                                                              col + site_index,
                                                                              '',
                                                                              f4)
                                                    site_index += 1
                                            if not week_sites:
                                                worksheet.merge_range(row + 1, col + team_index, row + 2,
                                                                      col + team_index,
                                                                      '',
                                                                      f4)
                                            team_index += 1
                                            row += 1
                                            if week_sites:
                                                worksheet.write(team_row + 1, col + team_index + len(week_sites) - 1,
                                                                str(site_index),
                                                                f3)
                                            else:
                                                worksheet.write(team_row + 1, col + team_index, str(site_index), f3)
                                        no_achieved += no_site_ok
                                        if week_sites:
                                            worksheet.write(team_row, col + team_index + len(week_sites) - 1, 'Total',
                                                            f3)
                                            worksheet.merge_range(row, col + team_index + len(week_sites) - 1, row + 1,
                                                                  col + team_index + len(week_sites) - 1,
                                                                  str(no_site_ok), f3)
                                        else:
                                            worksheet.write(team_row, col + team_index, 'Total', f3)
                                            worksheet.merge_range(row, col + team_index, row + 1,
                                                                  col + team_index, str(no_site_ok), f3)
                                            worksheet.merge_range(row, 0, row + 1, 0, 'Achieved', f2)
                                            row += 2
                                            worksheet.merge_range('I11:K12', 'Month Summary', f11)
                                            worksheet.write(10, 11, 'Plan', f2)
                                            worksheet.write(11, 11, 'Achieve', f2)
                                            worksheet.write(10, 12, str(no_planned), f2)
                                            worksheet.write(11, 12, str(no_achieved), f2)
