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

    import ipdb; ipdb.set_trace()

session.cr.commit()
session.cr.close()
