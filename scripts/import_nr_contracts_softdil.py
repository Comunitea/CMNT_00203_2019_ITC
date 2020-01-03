# -*- coding: utf-8 -*-
db_name = 'conecta'
session.open(db=db_name)
import logging
from odoo import fields
_logger = logging.getLogger(__name__)

def _parse_line(line):
    return {
        'extid': line[0],
        'name': line[1],
        'partner_extid': line[2],
        'partner_nif': line[3],
        'partner_name': line[4],
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

        'invoice_next_date': line[18],
        'line_product_extid': line[19],
        'line_product_name': line[20],
        'line_internal_reference': line[21],
        'line_description': line[22],
        'line_qty': line[23],
        'line_unit': line[24],
        'line_price': line[25],
        'line_discount': line[26],
        'user_name': line[27],
        # 'warn_percent': line[4],
        # 'recurring_each2': line[18],
        # 'mode_name': line[26],
        # 'term_name': line[27],
        # 'sale_type': line[28],
    }

def get_line_vals(data, idx, contract=False):
    import ipdb; ipdb.set_trace()
    field_lines = []
    product_id = False
    product = False
    if data.get('line_product_extid'):
        product = session.env.ref(data['line_product_extid'])
        if product:
            product_id = product.id
        else:
            logging.error('ERROR OBTENIENDO PARTNER %s EN (LIN %s)' % (data['partner_extid'], str(idx)))
    
    uom_id = False
    if data.get('line_unit'):
        domain = [('name', '=', data['line_unit'])]
        uom = session.env['uom.uom'].search(domain, limit=1)
        if uom:
            uom_id = uom.id
        else:
            logging.error('OBTENIENDO UOM %s EN (LIN %s)' % (data['line_unit'], str(idx)))
    date_start = False
    if data.get('date_start'):
        date_start = fields.Datetime.to_datetime(data.get('date_start'))
    date_end = False
    if data.get('date_end'):
        date_end = fields.Datetime.to_datetime(data.get('date_end'))
    
    if not date_start and contract:
        date_start = contract.contract_line_ids[0].date_start
    if not date_end and contract:
        date_end = contract.contract_line_ids[0].date_end
  
    recurring_interval = False
    if data.get('recurring_each'):
        recurring_interval = data.get('recurring_each')
    if not recurring_interval and contract:
        recurring_interval = contract.contract_line_ids[0].recurring_interval

    line_name = data.get('line_description')
    if not line_name and product:
        line_name = product.name_get()[0][1]
    recurring_rule_type = False
    if data.get('recurring_unit') or (contract and contract.contract_line_ids[0].recurring_rule_type):
        rt = data.get('recurring_unit') or contract.contract_line_ids[0].recurring_rule_type
        recurring_rule_type = rt
        if rt == 'Día(s)':
            recurring_rule_type = 'daily'
        elif rt == 'Semana(s)':
            recurring_rule_type = 'weekly'
        elif rt == 'Mes(es)':
            recurring_rule_type = 'monthly'
        elif rt == 'Mes(es) último día':
            recurring_rule_type = 'monthlylastdat'
        elif rt == 'Año(s)':
            recurring_rule_type = 'yearly'
        else:
            recurring_rule_type = rt

    recurring_next_date = False
    if data.get('invoice_next_date'):
        recurring_next_date = fields.Datetime.to_datetime(data.get('invoice_next_date'))
    if not recurring_next_date and contract:
        recurring_next_date = contract.contract_line_ids[0].recurring_next_date

    if not recurring_interval:
        logging.error('SIN RECURRING INTERVAL EN (LIN %s)' % (str(idx)))
    if not recurring_rule_type:
        logging.error('SIN RECURRING INTERVAL EN (LIN %s)' % (tr(idx)))
    if not recurring_next_date:
        logging.error('SIN RECURRING NEXT DATE EN (LIN %s)' % (str(idx)))
    
    qty_type = 'fixed'
    qty_formula_id = False
    if data.get('recurring_invoices')=='False':
        qty_formula_id = 3  # Analítica mismo producto
        # product_id = 950  # Analítica mismo producto PROD
        product_id = 329  # Analítica mismo producto
        uom_id = 6  # Horas
    elif not data.get(recurring_invoices) and contract:
        

    vals = {
        'product_id': product_id,
        'name': line_name,
        'recurring_interval': recurring_interval,
        'recurring_rule_type': recurring_rule_type,
        'date_start': date_start,
        'date_end': date_end,
        'recurring_next_date': recurring_next_date,
        'qty_type': qty_type,
        'qty_formula_id': qty_formula_id,
        'quantity': data.get('line_qty') or 0.0,
        'uom_id': uom_id,
        'price_unit': data.get('line_price') or 0.0,
        'discount': data.get('line_discount') or 0.0,

    }
    field_lines = [(0, 0, vals)]
    import ipdb; ipdb.set_trace()

    return field_lines

def get_contract_vals(data, idx):
    import ipdb; ipdb.set_trace()
    vals = {}
    field_lines = []

    partner_id = False
    # if data.get('partner_extid'):
    #     partner = session.env.ref(data['partner_extid'])
    #     if partner:
    #         partner_id = partner.id
    #     else:
    #         logging.error('OBTENIENDO PARTNER %s EN (LIN %s)' % (data['partner_extid'], str(idx)))
    
    partner_id = False
    if data.get('partner_nif'):
        partner = session.env['res.partner'].search([('vat', '=', data['partner_nif'])], limit=1)
        if partner:
            partner_id = partner.id
        else:
            partner_id = 7630  # CLIENTE Sin Nombre
            logging.error('OBTENIENDO PARTNER %s EN (LIN %s)' % (data['partner_extid'], str(idx)))
    
    user_id = False
    if data.get('user_name'):
        domain = [('name', '=', data['user_name'])]
        user = session.env['res.users'].search(domain, limit=1)
        if user:
            user_id = user.id
        else:
            logging.error('OBTENIENDO USUARIO %s EN (LIN %s)' % (data['user_name'], str(idx)))
    pricelist_id = False
    if data.get('pricelist_name'):
        domain = [('name', '=', data['pricelist_name'])]
        pricelist = session.env['product.pricelist'].search(domain, limit=1)
        if pricelist:
            pricelist_id = pricelist.id
        else:
            logging.error('OBTENIENDO TARIFA %s EN (LIN %s)' % (data['pricelist_name'], str(idx)))
    
    company_id = False
    if data.get('company_name'):
        domain = [('name', '=', data['company_name'])]
        company = session.env['res.company'].search(domain, limit=1)
        if company:
            company_id = company.id
        else:
            logging.error('OBETENIENDO COMPAÑÍA %s EN (LIN %s)' % (data['company_name'], str(idx)))

    payment_mode_id = False
    if data.get('mode_name'):
        domain = [('name', '=', data['mode_name'])]
        pm = session.env['account.payment.mode'].search(domain, limit=1)
        if pm:
            payment_mode_id = pm.id
        else:
            logging.error('OBETENIENDO MODO PAGO %s EN (LIN %s)' % (data['mode_name'], str(idx)))

    payment_term_id = False
    if data.get('term_name'):
        domain = [('name', '=', data['term_name'])]
        pt = session.env['account.payment.term'].search(domain, limit=1)
        if pt:
            payment_term_id = pt.id
        else:
            logging.error('OBTENIENDO PLAZO DE PAGO %s EN (LIN %s)' % (data['term_name'], str(idx)))

    journal_id = False
    # if data.get('sale_type'):
    #     domain = [('name', '=', data['sale_type'])]
    #     st = session.env['sale.order.type'].search(domain, limit=1)
    #     if st and st.journal_id:
    #         journal_id = st.journal_id.id
    #     else:
    #         logging.error('OBTENIENDO DIARO DE %s EN (LIN %s)' % (data['sale_type'], str(idx)))

    line_vals = get_line_vals(data, idx)
    vals = {
        'name': data.get('name'),
        'partner_id': partner_id,
        'user_id': user_id,
        'code': data.get('reference'),
        'warn_percent': data.get('warn_percent'),
        'quantity_max': data.get('quantity_max'),
        'description': data.get('description'),
        'company_id': 12,
        'pricelist_id': pricelist_id,
        'contract_line_ids': line_vals,
        'payment_mode_id': payment_mode_id,
        'payment_term_id': payment_term_id,
        'journal_id': journal_id,
    }
    import ipdb; ipdb.set_trace()
    return vals

def create_contracts(contract_datas):
    idx = 1
    row_count = len(contract_datas) + 1
    created_contracts = session.env['contract.contract']
    for data in contract_datas:
        idx += 1
        _logger.info('IMPORTANDO CONTRATO LÍNEA %s / %s' % (idx, row_count))
        ext_id = data.get('extid')
        cotract = False
        if ext_id:
            vals = get_contract_vals(data, idx)
            contract = session.env['contract.contract'].create(vals)
            created_contracts += contract
            data =  [{
                'xml_id': 'CONTRACTSOFT.' + ext_id.replace('.', '_'),
                'record': contract,
                'noupdate': True
            }]
            session.env['ir.model.data']._update_xmlids(data)
        else:
            line_vals = get_line_vals(data, idx, contract)
            contract.write({'contract_line_ids': line_vals})
    created_contracts.link_project()



import csv
idx = 0
f1 = open('/home/javier/buildouts/conecta/scripts/contratos_softdil.csv', newline='\n')
lines2count= csv.reader(f1, delimiter=',', quotechar='"')
row_count = sum(1 for row in lines2count)

with open('/home/javier/buildouts/conecta/scripts/contratos_softdil.csv', newline='\n') as csvfile:
    lines = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    contract_datas = []
    for line in lines:
        idx += 1
        if idx == 1:
            continue  # skip header
        _logger.info('LEYENDO LÍNEA %s / %s' % (idx, row_count))
        data= _parse_line(line)
        contract_datas.append(data)

    create_contracts(contract_datas)
    
# session.cr.commit()
# session.cr.close()
