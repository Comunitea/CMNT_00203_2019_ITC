# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.model
    def _get_task_vals(self, task, date_start, date_end, work_type):
        task_vals = {}
        value = {'presencial':3,'remoto':2,'telefonico':1,'taller':0,
                'lopd':0,'cmax':0,'interno':0}
        
        # Fecha respuesta y tipo resolucion, si es la fecha mas baja 
        # significa que tiene que ser el tipo de resolucion
        if task.reply_date:
            if date_start < task.reply_date:
                task_vals.update({
                    'reply_date': date_start,
                    'reply_type': work_type,
                })
            elif date_start == task.reply_date:
                task_vals.update({
                    'reply_type': work_type
                })
        elif value[work_type] > 0:
            task_vals.update({
                'reply_date': date_start,
                'reply_type': work_type,
            })
        
        # Fecha finalizado
        if task.finish_date:
            if date_end < task.finish_date:
                 task_vals['finish_date'] = date_end
        else:
            task_vals['finish_date'] = date_end
        
        # Cálculo del tipo de trabajo para tiempo de resolucion
        if task.resolution_type:
            if value[work_type] > value[task.resolution_type]:
                task_vals['resolution_type'] = work_type
        elif value[work_type] > 0:
            task_vals['resolution_type'] = work_type
        return task_vals

    @api.model
    def create(self, vals):
        
        if not vals.get('task_id', False):
            return res

        # TODO Comprobaciones diario y account_id?
        task = self.env['project.task'].browse(vals['task_id'])
        date_start = vals['date_start']
        date_end = vals['date_end']
        work_type = vals.get('work_type')
        
        task_vals = self._get_task_vals(
                task, date_start, date_end, work_type)
        if task_vals:
            task.write(task_vals)
        
        res = super().create(vals)
        return res
    
    @api.multi
    def write(self, vals):
        # import pdb; pdb.set_trace()
        res = super().write(vals)
        
        for work in self:
            if not work.task_id:
                continue

            task = work.task_id
            work_type = work.work_type
            date_start = work.date_start
            date_end = work.date_end
            if vals.get('work_type'):
                work_type = vals['work_type']
            if vals.get('date_start'):
                date_start = vals['date_start']

            task_vals = self._get_task_vals(
                task, date_start, date_end, work_type)
            if task_vals:
                work.task_id.write(task_vals)
        return res
    
    @api.multi
    def _check_reply_date(self):
        for work in self:
            if not work.task_id:
                continue
            task = work.task_id
            work_type = work.work_type
            date_start = work.date_start
            date_end = work.date_end

            task_vals = self._get_task_vals(
                task, date_start, date_end, work_type)
            if task_vals:
                work.task_id.write(task_vals)