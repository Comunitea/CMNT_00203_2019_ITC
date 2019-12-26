from odoo import fields, models, api
import math

class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    # From sd_timecontrol_dates
    #Overwrite date for Datetime
    date_start = fields.Datetime('Date Start')
    date_end = fields.Datetime('Date End')
    work_type = fields.Selection(
        [('presencial','Presencial'),
         ('remoto','Remoto'),
         ('telefonico','Telefonico'),
         ('taller','Taller'),
         ('lopd','LOPD'),
         ('cmax','CMAX'),
         ('interno','Interno')], 'Work Type')
    name = fields.Text('Description')
    discount = fields.Float('Hours discount')
    signature = fields.Binary('Customer signature')
    observations = fields.Text('Observations')
    sended = fields.Boolean('Sended', default=False)

    @api.onchange('date_start', 'date_end', 'work_type', 'discount')
    def _on_change_datetime(self):
        self.ensure_one()
        res = 0
        if self.date_start and self.date_end and self.work_type:
            diff = self.date_end - self.date_start
            hours = ( (diff.seconds) / 3600)
            decimals = hours - math.floor(hours)
            hours_floor = math.floor( (hours * 10) + 0.89) / 10

            if (self.work_type == 'presencial'):
                if(hours < 1 and hours > 0):
                    res = 1
                else:
                    res = round(2 * hours_floor + 0.499) / 2
            
            elif self.work_type in ['remoto', 'telefonico', 'taller', 'cmax']:
                if(decimals == 0):
                    res = math.floor(hours)
                elif(decimals > 0 and decimals <= 0.25):
                    res = math.floor(hours) + 0.25
                elif (decimals > 0.25 and decimals <= 0.5):
                    res = math.floor(hours) + 0.5
                elif(decimals > 0.5 and decimals <= 0.75):
                    res = math.floor(hours) + 0.75
                elif(decimals > 0.75 and decimals <= 1):
                    res = math.floor(hours) + 1
                else:
                    res = hours
            self.unit_amount = res - self.discount
    
    @api.model
    def create(self, vals):
        res = super().create(vals)
        import ipdb; ipdb.set_trace()
        if res.task_id and res.task_id.contract_id:
            contract = res.task_id.contract_id
            if contract.check_limit():
                self.send_warning_mail(contract.id)
        return res
    
    def send_warning_mail(self, account_id):
        email_template_warn = self.env.ref('custom_timecontrol_dates.email_template_warn')
        email_template_warn.send_mail(account_id, force_send=True)
        return True
    
    # def invoice_cost_create(self, cr, uid, ids, data=None, context=None):
    # 			analytic_account_obj = self.pool.get('account.analytic.account')
    # 			account_payment_term_obj = self.pool.get('account.payment.term')
    # 			invoice_obj = self.pool.get('account.invoice')
    # 			product_obj = self.pool.get('product.product')
    # 			invoice_factor_obj = self.pool.get('hr_timesheet_invoice.factor')
    # 			fiscal_pos_obj = self.pool.get('account.fiscal.position')
    # 			product_uom_obj = self.pool.get('product.uom')
    # 			invoice_line_obj = self.pool.get('account.invoice.line')
    # 			invoices = []
    # 			if context is None:
    # 					context = {}
    # 			if data is None:
    # 					data = {}

    # 			journal_types = {}

    # 			# prepare for iteration on journal and accounts
    # 			for line in self.pool.get('account.analytic.line').browse(cr, uid, ids, context=context):
    # 					if line.journal_id.type not in journal_types:
    # 							journal_types[line.journal_id.type] = set()
    # 					journal_types[line.journal_id.type].add(line.account_id.id)
    # 			for journal_type, account_ids in journal_types.items():
    # 					for account in analytic_account_obj.browse(cr, uid, list(account_ids), context=context):
    # 							partner = account.partner_id
    # 							if (not partner) or not (account.pricelist_id):
    # 									raise osv.except_osv(_('Analytic Account Incomplete!'),
    # 													_('Contract incomplete. Please fill in the Customer and Pricelist fields.'))

    # 							date_due = False
    # 							if partner.property_payment_term:
    # 									pterm_list= account_payment_term_obj.compute(cr, uid,
    # 													partner.property_payment_term.id, value=1,
    # 													date_ref=time.strftime('%Y-%m-%d'))
    # 									if pterm_list:
    # 											pterm_list = [line[0] for line in pterm_list]
    # 											pterm_list.sort()
    # 											date_due = pterm_list[-1]

    # 							if account.payment_term_id:
    # 								payment_term = account.payment_term_id.id
    # 							elif partner.property_payment_term:
    # 								payment_term = partner.property_payment_term.id
    # 							else:
    # 								payment_term = False

    # 							if account.payment_mode_id:
    # 								payment_mode = account.payment_mode_id.id
    # 							elif partner.customer_payment_mode:
    # 								payment_mode = partner.customer_payment_mode.id
    # 							else:
    # 								payment_mode = False

    # 							curr_invoice = {
    # 									'name': time.strftime('%d/%m/%Y') + ' - '+account.name,
    # 									'partner_id': account.partner_id.id,
    # 									'company_id': account.company_id.id,
    # 									'payment_term': payment_term,
    # 									'payment_mode_id': payment_mode,
    # 									'account_id': partner.property_account_receivable.id,
    # 									'currency_id': account.pricelist_id.currency_id.id,
    # 									'date_due': date_due,
    # 									'fiscal_position': account.partner_id.property_account_position.id,
    #                                                                             'journal_id': account.type_id.journal_id.id,
    # 							}
    # 							context2 = context.copy()
    # 							context2['lang'] = partner.lang
    # 							# set company_id in context, so the correct default journal will be selected
    # 							context2['force_company'] = curr_invoice['company_id']
    # 							# set force_company in context so the correct product properties are selected (eg. income account)
    # 							context2['company_id'] = curr_invoice['company_id']

    # 							last_invoice = invoice_obj.create(cr, uid, curr_invoice, context=context2)
    # 							invoices.append(last_invoice)

    # 							cr.execute("""SELECT line.id, product_id, user_id, to_invoice, amount, unit_amount, product_uom_id
    # 											FROM account_analytic_line as line LEFT JOIN account_analytic_journal journal ON (line.journal_id = journal.id)
    # 											WHERE account_id = %s
    # 													AND line.id IN %s AND journal.type = %s AND to_invoice IS NOT NULL
    # 											GROUP BY line.id, product_id, user_id, to_invoice, amount, unit_amount, product_uom_id
    #                                                                                             ORDER BY fecha_inicio ASC""", (account.id, tuple(ids), journal_type))

    # 							"""QUITA COMENTARIO"""
    # 							for line_id, product_id, user_id, factor_id, total_price, qty, uom in cr.fetchall():
    # 									context2.update({'uom': uom})

    # 									if data.get('product'):
    # 											# force product, use its public price
    # 											product_id = data['product'][0]
    # 											unit_price = self._get_invoice_price(cr, uid, account, product_id, user_id, qty, context2)
    # 									elif journal_type == 'general' and product_id:
    # 											# timesheets, use sale price
    # 											unit_price = self._get_invoice_price(cr, uid, account, product_id, user_id, qty, context2)
    # 									else:
    # 											# expenses, using price from amount field
    # 											unit_price = total_price*-1.0 / qty

    # 									factor = invoice_factor_obj.browse(cr, uid, factor_id, context=context2)
    # 									# factor_name = factor.customer_name and line_name + ' - ' + factor.customer_name or line_name
    # 									factor_name = factor.customer_name
    # 									curr_line = {
    # 											'price_unit': unit_price,
    # 											'quantity': qty,
    # 											'product_id': product_id or False,
    # 											'discount': factor.factor,
    # 											'invoice_id': last_invoice,
    # 											'name': factor_name,
    # 											'uos_id': uom,
    # 											'account_analytic_id': account.id,
    # 									}
    # 									product = product_obj.browse(cr, uid, product_id, context=context2)
    # 									if product:
    # 											factor_name = product_obj.name_get(cr, uid, [product_id], context=context2)[0][1]
    # 											if factor.customer_name:
    # 													factor_name += ' - ' + factor.customer_name
    # 											general_account = product.property_account_income or product.categ_id.property_account_income_categ
    # 											if not general_account:
    # 													raise osv.except_osv(_("Configuration Error!"), _("Please define income account for product '%s'.") % product.name)
    # 											taxes = product.taxes_id or general_account.tax_ids
    # 											tax = fiscal_pos_obj.map_tax(cr, uid, account.partner_id.property_account_position, taxes)
    # 											curr_line.update({
    # 													'invoice_line_tax_id': [(6,0,tax )],
    # 													'name': factor_name,
    # 													'invoice_line_tax_id': [(6,0,tax)],
    # 													'account_id': general_account.id,
    # 											})
    # 									#
    # 									# Compute for lines
    # 									#
    # 									cr.execute("""SELECT line.product_uom_id, line.fecha_inicio fecha_inicio,
    #                                                         line.fecha_fin fecha_fin, line.tipo_trabajo,
    #                                                         line.unit_amount, line.descuento, line.name, timesheet.issue_id, issue.description, partner.name as tecnico
    #                                                     FROM account_analytic_line line INNER JOIN 
    #                                                         hr_analytic_timesheet timesheet ON line.id = timesheet.line_id INNER JOIN
    #                                                         project_issue issue ON timesheet.issue_id = issue.id INNER JOIN
    #                                                         res_users users ON users.id = line.user_id INNER JOIN
    #                                                         res_partner partner ON partner.id = users.partner_id
    #                                                     WHERE line.account_id = %s and line.id = %s AND 
    #                                                         line.product_id=%s and line.to_invoice=%s AND line.invoice_id IS NULL
    #                                                     ORDER BY line.fecha_inicio ASC, issue_id ASC;""", (account.id, line_id, product_id, factor_id))

    # 									line_ids = cr.dictfetchall()
    # 									for line in line_ids:
    # 											note = []
    # 											details = []
    # 											curr_line.update({
    # 													'name': '',
    # 											})
    # 											if line['issue_id']:
    # 													details.append("INCIDENCIA: %s - %s" % (line['issue_id'], line['description'], ))
    # 											if data.get('date', False):
    #                                                                                                             timezone = pytz.timezone('Europe/Madrid')

    #                                                                                                             fecha_inicio = datetime.strptime(line['fecha_inicio'], '%Y-%m-%d %H:%M:%S')
    #                                                                                                             fecha_inicio = fecha_inicio.replace(tzinfo=pytz.utc)
    #                                                                                                             fecha_inicio = fecha_inicio.astimezone(timezone)
    #                                                                                                             fecha_inicio_dt = timezone.normalize(fecha_inicio)

    #                                                                                                             fecha_fin = datetime.strptime(line['fecha_fin'], '%Y-%m-%d %H:%M:%S')
    #                                                                                                             fecha_fin = fecha_fin.replace(tzinfo=pytz.utc)
    #                                                                                                             fecha_fin = fecha_fin.astimezone(timezone)
    #                                                                                                             fecha_fin_dt = timezone.normalize(fecha_fin)

    # 													details.append("\nFecha inicio: %s \nFecha fin: %s" % (fecha_inicio_dt, fecha_fin_dt, ))
    # 											if data.get('time', False):
    # 													if line['tipo_trabajo']:
    # 															details.append("\nTipo trabajo: %s" % (line['tipo_trabajo'], ))
    # 													if line['product_uom_id']:
    # 															details.append("\nTotal: %s %s" % (line['unit_amount'], product_uom_obj.browse(cr, uid, [line['product_uom_id']],context2)[0].name))
    # 													else:
    # 															details.append("\nTotal: %s" % (line['unit_amount'], ))
    # 													if line['descuento']:
    # 															details.append("\nDescontadas: %s" % (line['descuento'], ))
    # 											if data.get('name', False):
    # 													details.append("\nTrabajo realizado:\n%s" % (line['name'], ))
    # 											if line.get('tecnico', False):
    # 													details.append("\nRealizado por: %s" % (line['tecnico'], ))
    # 											note.append(u''.join(map(lambda x: unicode(x) or '', details)))
    # 											if note:
    # 													curr_line['name'] += ("\n".join(map(lambda x: unicode(x) or '',note)))
    # 											invoice_line_obj.create(cr, uid, curr_line, context=context)
    # 											cr.execute("update account_analytic_line set invoice_id=%s WHERE account_id = %s and id = %s", (last_invoice, account.id, line_id))
    # 									self.invalidate_cache(cr, uid, ['invoice_id'], ids, context=context)


    # 							invoice_obj.button_reset_taxes(cr, uid, [last_invoice], context)
    # 			return invoices
    
