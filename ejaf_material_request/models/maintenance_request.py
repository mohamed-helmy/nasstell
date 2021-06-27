from odoo import api, fields, models, _


class ActualMaterialUsed(models.Model):
    _name = 'actual.material.used'
    _description = 'Actual Material Used'

    product_id = fields.Many2one('product.product', string='Product')
    requested_qty = fields.Integer(string='Requested Qty')
    actual_qty = fields.Integer(string='Actual Qty')
    returned_qty = fields.Integer(string='Returned Qty')
    requested_uom = fields.Char(string='Unit Of Measure')
    actual_uom = fields.Char(string='Unit Of Measure')
    returned_uom = fields.Char(string='Unit Of Measure')
    requested_serials = fields.Char(string='Serial No')
    actual_serials = fields.Char(string='Serial No')
    requested_product_status = fields.Char(string='Product Status')
    actual_product_status = fields.Char(string='Product Status')
    returned_serials = fields.Char(string='Serial No')
    returned_product_status = fields.Char(string='Product Status')


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    material_request_ids = fields.One2many('material.request', 'maintenance_request_id', string='Material Requests')
    material_request_line_ids = fields.Many2many('actual.material.used', 'actual_material_rel', 'material_req_id',
                                                 'maintenance_id', string='Requested & Returned Material',
                                                 compute='get_material_lines')
    actual_material_used_ids = fields.Many2many('actual.material.used', 'actual_material_used_rel',
                                                'actual_material_req_id',
                                                'maintenance_id', string='Actual Material Used',
                                                compute='get_actual_material_used')

    material_request_count = fields.Integer(compute='calc_material_requests')
    returned_material_request_count = fields.Integer(compute='calc_returned_material_requests')

    @api.depends('material_request_ids')
    def get_actual_material_used(self):
        for req in self:
            actual_lines = []
            products = []
            data = []
            returned_serials = []
            if req.material_request_ids:
                for material in req.material_request_ids.filtered(lambda mm: mm.state == 'transferred' and mm.line_ids):
                    for line in material.line_ids.filtered(
                            lambda ll: ll.returned and ll.lot_id.id not in returned_serials):
                        returned_serials.append(line.lot_id.id)

            if req.material_request_ids:
                for material in req.material_request_ids.filtered(lambda mm: mm.state == 'transferred' and mm.line_ids):
                    for line in material.line_ids.filtered(lambda ll: not ll.returned):
                        move_line = material.picking_id.move_line_ids_without_package.filtered(lambda
                                                                                                   ll: ll.product_id.id == line.product_id.id and ll.picking_id.id == material.picking_id.id)
                        if move_line and move_line[0].lot_id and move_line[0].lot_id.id not in returned_serials:
                            created_obj = self.env['actual.material.used'].sudo().create({
                                'product_id': line.product_id.id,
                                'actual_qty': line.qty,
                                'actual_serials': move_line[0].lot_id.name if move_line and move_line[0].lot_id else '',
                                'actual_product_status': move_line[0].product_status if move_line and move_line[
                                    0].product_status else '',
                                'actual_uom': move_line[0].product_uom_id.name if move_line and move_line[
                                    0].product_uom_id else '',
                            })
                            actual_lines.append(created_obj.id)
            req.actual_material_used_ids = actual_lines

    @api.depends('material_request_ids')
    def get_material_lines(self):
        for req in self:
            print("hhhhhhhhhhhhhh")
            material_lines = []
            data = {}
            if req.material_request_ids:
                for material in req.material_request_ids.filtered(lambda mm: mm.state == 'transferred' and mm.line_ids):
                    for line in material.line_ids:
                        stock_move_lines = material.picking_id.move_line_ids_without_package.filtered(lambda
                                                                                                          ll: ll.product_id.id == line.product_id.id and ll.picking_id.id == material.picking_id.id)
                        if line.product_id and line.product_id.id not in data.keys():
                            product_data = []
                            if line.returned:
                                for stock_move_line in stock_move_lines:
                                    product_data.append({'requested': 0,
                                                         'requested_serial': '',
                                                         'requested_product_status': '',
                                                         'requested_uom': '',
                                                         'returned': stock_move_line.qty_done,
                                                         'returned_serial': stock_move_line.lot_id.name if stock_move_line and stock_move_line.lot_id else '',
                                                         'returned_product_status': stock_move_line.product_status if stock_move_line and stock_move_line.product_status else '',
                                                         'returned_uom': ''})
                            else:
                                for stock_move_line in stock_move_lines:
                                    product_data.append({'requested': stock_move_line.qty_done,
                                                         'requested_serial': stock_move_line.lot_id.name if stock_move_line and stock_move_line.lot_id else '',
                                                         'requested_product_status': stock_move_line.product_status if stock_move_line and stock_move_line.product_status else '',
                                                         'requested_uom': stock_move_line.product_uom_id.name if stock_move_line and stock_move_line.product_uom_id else '',
                                                         'returned': 0,
                                                         'returned_serial': '',
                                                         'returned_uom': '',
                                                         'returned_product_status': ''})
                            data[line.product_id.id] = product_data
                        else:
                            for stock_move_line in stock_move_lines:
                                data[line.product_id.id].append({'requested': stock_move_line.qty_done,
                                                     'requested_serial': stock_move_line.lot_id.name if stock_move_line and stock_move_line.lot_id else '',
                                                     'requested_product_status': stock_move_line.product_status if stock_move_line and stock_move_line.product_status else '',
                                                     'requested_uom': stock_move_line.product_uom_id.name if stock_move_line and stock_move_line.product_uom_id else '',
                                                     'returned': 0,
                                                     'returned_serial': '',
                                                     'returned_uom': '',
                                                     'returned_product_status': ''})
                            # if not line.returned:
                                # for element in data[line.product_id.id]:
                                    # if element['requested'] > 0:
                                        # for stock_move_line in stock_move_lines:
                                        #     element['requested'] += stock_move_line.qty_done
                                            # if stock_move_line and stock_move_line[0].lot_id and stock_move_line[
                                            #     0].lot_id.name not in \
                                            #         element['requested_serial']:
                                            #     element[
                                            #         'requested_serial'] += ',' + stock_move_line[
                                            #         0].lot_id.name if stock_move_line and stock_move_line[0].lot_id else ''
                                            # if stock_move_line and stock_move_line[0].product_uom_id and stock_move_line[
                                            #     0].product_uom_id.name not in \
                                            #         element['requested_uom']:
                                            #     element[
                                            #         'requested_uom'] += ',' + stock_move_line[
                                            #         0].product_uom_id.name if stock_move_line and stock_move_line[
                                            #         0].product_uom_id else ''
                                            # if stock_move_line and stock_move_line[0].lot_id and stock_move_line[
                                            #     0].product_status not in \
                                            #         element['requested_product_status']:
                                            #     element[
                                            #         'requested_product_status'] += ',' + stock_move_line[
                                            #         0].product_status if stock_move_line and stock_move_line[
                                            #         0].product_status else ''
                            if line.returned:
                                # if data[line.product_id.id][0][
                                #     'returned_uom'] and stock_move_line and stock_move_line.product_uom_id.name not in \
                                #         data[line.product_id.id][0]['returned_uom']:
                                #     data[line.product_id.id][0][
                                #         'returned_uom'] += ',' + stock_move_line[0].product_uom_id.name
                                # else:
                                #     data[line.product_id.id][0][
                                #         'returned_uom'] = stock_move_line[0].product_uom_id.name if stock_move_line and \
                                #                                                                     stock_move_line[
                                #                                                                         0].product_uom_id else ''
                                for stock_move_line in stock_move_lines:
                                    if stock_move_line and stock_move_line.lot_id.name in \
                                            data[line.product_id.id][0][
                                                'requested_serial']:
                                        if data[line.product_id.id][0]['returned_serial']:
                                            if stock_move_line and stock_move_line.lot_id.name not in \
                                                    data[line.product_id.id][0][
                                                        'returned_serial']:
                                                data[line.product_id.id][0][
                                                    'returned_serial'] += ',' + stock_move_line.lot_id.name
                                        else:
                                            data[line.product_id.id][0][
                                                'returned_serial'] = stock_move_line.lot_id.name
                                        if data[line.product_id.id][0]['returned_product_status']:
                                            data[line.product_id.id][0][
                                                'returned_product_status'] += ',' + stock_move_line.product_status
                                        else:
                                            data[line.product_id.id][0][
                                                'returned_product_status'] = stock_move_line.product_status
                                        data[line.product_id.id][0]['returned'] += stock_move_line.qty_done
                                    else:
                                        data[line.product_id.id].append({
                                            'requested': 0,
                                            'requested_serial': '',
                                            'requested_product_status': '',
                                            'requested_uom': '',
                                            'returned': stock_move_line.qty_done,
                                            'returned_serial': stock_move_line.lot_id.name if stock_move_line and
                                                                                                 stock_move_line.lot_id else '',
                                            'returned_product_status': stock_move_line.product_status if stock_move_line and stock_move_line.product_status else '',
                                            'returned_uom': stock_move_line.product_uom_id.name if stock_move_line and
                                                                          stock_move_line.product_uom_id else ''
                                        })
            for key, value in data.items():
                for item in value:
                    created_obj = self.env['actual.material.used'].sudo().create({
                        'product_id': key,
                        'requested_qty': item['requested'],
                        'requested_serials': item['requested_serial'],
                        'requested_product_status': item['requested_product_status'],
                        'requested_uom': item['requested_uom'],
                        'returned_qty': item['returned'],
                        'returned_serials': item['returned_serial'],
                        'returned_uom': item['returned_uom'],
                        'returned_product_status': item['returned_product_status'], })
                    material_lines.append(created_obj.id)
            req.material_request_line_ids = material_lines

    def calc_material_requests(self):
        for maintenance in self:
            maintenance.material_request_count = len(maintenance.material_request_ids.filtered(lambda m: not m.returned))

    def action_view_material_requests(self):
        return {
            'name': _('Material Requests'),
            'res_model': 'material.request',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('ejaf_material_request.material_request_tree_view').id, 'tree'),
                (self.env.ref('ejaf_material_request.material_request_form_view').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'domain': [('maintenance_request_id', '=', self.id), ('returned', '=', False)],
            'context': {'default_maintenance_request_id': self.id, 'default_returned': False}
        }

    def calc_returned_material_requests(self):
        self.returned_material_request_count = len(self.material_request_ids.filtered(lambda m: m.returned))

    def action_view_returned_material_requests(self):
        return {
            'name': _('Returned Material Requests'),
            'res_model': 'material.request',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('ejaf_material_request.material_request_tree_view').id, 'tree'),
                (self.env.ref('ejaf_material_request.material_request_form_view').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'domain': [('maintenance_request_id', '=', self.id), ('returned', '=', True)],
            'context': {'default_maintenance_request_id': self.id, 'default_returned': True}
        }
