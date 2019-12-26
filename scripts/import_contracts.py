# -*- coding: utf-8 -*-
db_name = 'conecta_testing'
session.open(db=db_name)
import logging
_logger = logging.getLogger(__name__)

def _parse_line(line):
    return {
        'extid': line[0],
        'name': line[1],
        'partner_extid': line[2],
        'user_name': line[3],
        'warn_percent': line[4],
        'reference': line[5],
        'company_name': line[6],
        'date_start': line[7],
        'date_end': line[8],
        'fix_price': line[9],
        'amount_max': line[10],
        'quantity_max': line[11],
        'invoice_timesheets': line[12],
        'pricelist_name': line[13],
        'recurring_invoices': line[14],
        'description': line[15],
        'recurring_unit': line[16],
        'recurring_each': line[17],
        'recurring_each2': line[18],
        'invoice_next_date': line[19],
        'line_product_extid': line[20],
        'line_description': line[21],
        'line_qty': line[22],
        'line_unit': line[23],
        'line_price': line[24],
        'line_discount': line[25],
    }

def get_line_vals(data):
    field_lines = []
    product_id = False
    uom_id = False
    date_start = False
    date_end = False
    recurring_rule_type = False
    vals = {
        'product_id': product_id,
        'recurring_interval': data.get('recurring_interval'),
        'recurring_rule_type': recurring_rule_type,
        'date_start': data.get('recurring_interval'),
        'date_end': data.get('recurring_interval'),
        'recurring_next_date': data.get('recurring_interval'),
        'qty_type': 'fixed',
        'quantity': data.get('line_qty'),
        'uom_id': uom_id,
        'price_unit': data.get('line_price'),
        'discount': data.get('line_discount'),

    }
    field_lines = [(0, 0, vals)]
    return field_lines

def get_contract_vals(data):
    field_lines = []
    partner_id = False
    user_id = False
    pricelist_id = False

    line_vals = get_line_vals(data)
    vals = {
        'name': data.get('name'),
        'partner_id': partner_id,
        'user_id': user_id,
        'reference': data.get('reference'),
        'warn_percent': data.get('warn_percent'),
        'quantity_max': data.get('quantity_max'),
        # 'company_id': company_id,
        'pricelist_id': pricelist_id
        'contract_line_ids': line_vals
    }

def create_contracts(contract_datas):
    import ipdb; ipdb.set_trace()
    for data in contract_datas:
        ext_id = data.get('ext_id')
        cotract = False
        if ext_id:
            vals = self.get_contract_vals(data)
            contract = self.env['contract.contract'].create(vals)
        else:
            line_vals = get_line_vals(data)
            contract.write({'contract_line_ids': line_vals})



import csv
idx = 0
import ipdb; ipdb.set_trace()
f1 = open('/home/javier/buildouts/conecta/scripts/contratos.csv', newline='\n')
lines2count= csv.reader(f1, delimiter=',', quotechar='"')
row_count = sum(1 for row in lines2count)

with open('/home/javier/buildouts/conecta/scripts/contratos.csv', newline='\n') as csvfile:
    lines = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    contract_datas = []
    for line in lines:
        idx += 1
        if idx == 1:
            continue  # skip header
        _logger.info('IMPORTANDO LÍNEA %s / %s' % (idx, row_count))
        data= _parse_line(line)
        contract_datas.append(data)

    create_contracts(contract_datas)
    
session.cr.commit()
session.cr.close()
