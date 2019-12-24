# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = ['project.task']

    signature = fields.Binary("Firma del cliente")

    @api.model
    def create(self, vals):
        res = super().create(vals)
        # TODO
        # if 'project_id' in vals:
        #     project = self.env['project.project'].browse(vals['project_id']):
        #     if project.analytic_account_id:
        #         if project.analytic_account_id.check_limit():
        #             self.send_warning_mail(project.analytic_account_id.id)
        return res
    
    #  def enviar_correo_aviso(self, cr, uid, ids, context=None):
    #     email_template_obj = self.pool.get('email.template')
    #     template_ids = email_template_obj.search(cr, uid, [('name','=','Aviso exceso')], limit=1)
    #     for template_id in template_ids:
    #         for contract in self.pool.get('account.analytic.account').browse(cr, uid, ids, context=context):
    #             email_template_obj.send_mail(cr, uid, template_id, contract.id, context=context)
    #     return True

    @api.model
    def create(self, vals):
        res = super().create(vals)
        # TODO SEND MAIL WARNING
        # if 'account_id' in vals:
        #     account = self.env['account.analytic.account'].browse(vals['account_id'])
		# 	if account.check_limit():
		# 		self.send_warning_mail(account.id)
        return res
    
    def send_warning_mail(self, account_id):
        # email_template_obj = self.pool.get('email.template')
        # template_ids = email_template_obj.search(cr, uid, [('name','=','Aviso exceso')], limit=1)
        # for template_id in template_ids:
        #     for contract in self.pool.get('account.analytic.account').browse(cr, uid, ids, context=context):
        #         email_template_obj.send_mail(cr, uid, template_id, contract.id, context=context)
  
        email_template_warn = self.env.ref('custom_timecontrol_dates.email_template_warn')
        email_template_warn.send_mail(account_id, force_send=True)
        return True