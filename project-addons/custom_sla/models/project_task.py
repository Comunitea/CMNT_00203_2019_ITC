# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = ['project.task', 'project.sla.controlled']
    _name = 'project.task'

    @api.multi
    @api.depends('timesheet_ids.date_end')
    def _compute_final(self):
        for task in self:
            finish_date = False
            for ts in task.timesheet_ids:
                if not ts.date_end:
                    continue
                if finish_date == False:
                    finish_date = ts.date_end
                elif finish_date < ts.date_end:
                    finish_date = ts.date_end
            task.last_task_date = finish_date
    
    # OVERWRITED
    @api.multi
    @api.depends('issue_date', 'last_task_date', 'reply_date')
    def _compute_elapsed(self):
        """
        Sobreescribo y cambio date_assign por reply_date y date_end por
        last_task_date, date_create por issue_date

        """
        task_linked_to_calendar = self.filtered(
            lambda task: task.project_id.resource_calendar_id and task.issue_date
        )
        for task in task_linked_to_calendar:
            # isue_date by create_date
            dt_create_date = fields.Datetime.from_string(task.issue_date)

            if task.reply_date:
                dt_date_assign = fields.Datetime.from_string(task.reply_date)
                task.working_hours_open = task.project_id.resource_calendar_id.get_work_hours_count(
                        dt_create_date, dt_date_assign, compute_leaves=True)
                task.working_days_open = task.working_hours_open / 24.0

            if task.last_task_date:
                dt_date_end = fields.Datetime.from_string(task.last_task_date)
                task.working_hours_close = task.project_id.resource_calendar_id.get_work_hours_count(
                    dt_create_date, dt_date_end, compute_leaves=True)
                task.working_days_close = task.working_hours_close / 24.0

        (self - task_linked_to_calendar).update(dict.fromkeys(
            ['working_hours_open', 'working_hours_close', 'working_days_open', 'working_days_close'], 0.0))

    # Fields from sd_project_sla module
    waiting = fields.Boolean('Esperando')
    finish_date = fields.Datetime('Finalizado', readonly=True, select=True)
    last_task_date = fields.Datetime(
        compute='_compute_final', 
        string="Fecha finalización de última tarea", 
        store=True)
    # Field from project_issue module
    date_closed = fields.Datetime('Closed', readonly=True, select=True)

    # From sd_ajustes_conecta
    reply_date = fields.Datetime('Fecha de respuesta')
    reply_type = fields.Char('Tipo respuesta')
    resolution_type = fields.Char('Tipo resolucion')

    # is_issue = fields.Boolean('Es incidencia')
    issue_date = fields.Datetime(
        string="Fecha de la incidencia", required=True,
        default=fields.Datetime.now())
    notice_person = fields.Char(string="Persona de aviso", required=True)
    priority = fields.Selection(
        [('0','No procede'), ('1','Baja'), ('2','Media'), ('3','Alta')], 
        'Priority', select=True, index=True)
    problem = fields.Boolean('Problema')
    problem_description = fields.Text('Causa del problema')
    # project_id = fields.Many2one(
    # 'project.project', 'Project', track_visibility='onchange', select=True)
    # working_hours_open = fields.Float(
    #     compute='_compute_day', string='Working Hours to assign the Issue',
    #     store=True)
    # working_hours_close = fields.Float(
    #     compute='_compute_day', string='Working Hours to close the Issue',
    #     store=True)
    
    @api.onchange('stage_id')
    def onchange_stage_id(self):
        res = {}
        if not self.stage_id:
            return
        stage = self.stage_id
        if stage.name == 'Finalizada' or stage.name == 'Done' or \
                stage.name == 'Finalizado':
            self.finish_date = fields.Datetime.Now()
    
        elif stage.name == 'Esperando':
            self.waiting = True
        else:
            self.date_closed = False
        return
    
    # From project_issue_sheet
    #  def on_change_account_id(self, cr, uid, ids, account_id, context=None):
    #     if not account_id:
    #         return {}

    #     account = self.pool.get('account.analytic.account').browse(cr, uid, account_id, context=context)
    #     result = {}

    #     if account and account.state == 'pending':
    #         result = {'warning' : {'title' : _('Analytic Account'), 'message' : _('The Analytic Account is pending !')}}

    #     if account and account.remaining_hours < 0:
    #         result = {'warning' : {'title' : _('Analytic Account'), 'message' : _('El contrato tiene excesos de tiempo !')}}
            
    #     return result

    # From sd_ajustes_conecta
