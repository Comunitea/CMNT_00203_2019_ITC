# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# from __future__ import division
# import time
# from datetime import datetime

# from openerp.osv import fields
# from openerp.osv import osv
# from openerp.tools.translate import _
# from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
# import pytz
from odoo import fields, models, api


# class AccountAnalyticAccount(models.Model):
# 	_inherit = "account.analytic.account"

# 	def _discount(self):
# 		dp = 2
# 		res = {}
# 		parent_ids = tuple(ids)
# 		accounts = self.browse(cr, uid, ids, context=context)
# 		for id in ids:
# 			res[id] = 0.0
# 		if parent_ids:
# 			cr.execute("SELECT account_analytic_line.account_id, COALESCE(SUM(descuento), 0.0) \
# 					FROM account_analytic_line \
# 					JOIN account_analytic_journal \
# 						ON account_analytic_line.journal_id = account_analytic_journal.id \
# 					INNER JOIN account_analytic_account \
# 						ON account_analytic_account.id = account_analytic_line.account_id \
# 					WHERE account_analytic_line.account_id IN %s \
# 						AND account_analytic_journal.type='general' \
# 						AND account_analytic_line.fecha_inicio >= account_analytic_account.date_start \
# 						AND account_analytic_line.fecha_inicio < (account_analytic_account.date::date + '1 day'::interval) \
# 					GROUP BY account_analytic_line.account_id",(parent_ids,))
# 			ff =  cr.fetchall()
# 			for account_id, hq in ff:
# 				res[account_id] = round(hq, dp)
# 		for id in ids:
# 			res[id] = round(res[id], dp)
# 		return res

# 	def _hours_quantity(self, cr, uid, ids, fields, arg, context=None):
# 		dp = 2
# 		res = {}
# 		parent_ids = tuple(ids) #We don't want consolidation for each of these fields because those complex computation is resource-greedy.
# 		accounts = self.browse(cr, uid, ids, context=context)

# 		for id in ids:
# 			res[id] = 0.0
# 		if parent_ids:
# 			cr.execute("SELECT account_analytic_line.account_id, COALESCE(SUM(unit_amount), 0.0) \
# 					FROM account_analytic_line \
# 					JOIN account_analytic_journal \
# 						ON account_analytic_line.journal_id = account_analytic_journal.id \
# 					INNER JOIN account_analytic_account \
# 						ON account_analytic_account.id = account_analytic_line.account_id \
# 					WHERE account_analytic_line.account_id IN %s \
# 						AND account_analytic_journal.type='general' \
# 						AND account_analytic_line.fecha_inicio >= account_analytic_account.date_start \
# 						AND account_analytic_line.fecha_inicio < (account_analytic_account.date::date + '1 day'::interval) \
# 					GROUP BY account_analytic_line.account_id",(parent_ids,))
# 			ff =  cr.fetchall()
# 			for account_id, hq in ff:
# 				res[account_id] = round(hq, dp)
# 		for id in ids:
# 			res[id] = round(res[id], dp)
# 		return res
		
# 	_columns = {
# 		'total_descuento': fields.function(_descuento, type='float', string='Tiempo descontado total', method=True),
# 		'hours_quantity': fields.function(_hours_quantity, type='float', string='Total Worked Time', help="Number of time you spent on the analytic account (from timesheet). It computes quantities on all journal of type 'general'."),

# 	}
