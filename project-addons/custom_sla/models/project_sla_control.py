# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, SUPERUSER_ID, api
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DT_FMT
from datetime import datetime as dt
from . import m2m

import logging
_logger = logging.getLogger(__name__)


SLA_STATES = [('5', 'Failed'), ('4', 'Will Fail'), ('3', 'Warning'),
              ('2', 'Watching'), ('1', 'Achieved')]


def safe_getattr(obj, dotattr, default=False):
    """
    Follow an object attribute dot-notation chain to find the leaf value.
    If any attribute doesn't exist or has no value, just return False.
    Checks hasattr ahead, to avoid ORM Browse log warnings.
    """
    attrs = dotattr.split('.')
    while attrs:
        attr = attrs.pop(0)
        if attr in obj._fields:
            try:
                obj = getattr(obj, attr)
            except AttributeError:
                return default
            if not obj:
                return default
        else:
            return default
    return obj


class ProjectSlaControl(models.Model):
    """
    SLA Control Registry
    Each controlled document (Issue, Claim, ...) will have a record here.
    This model concentrates all the logic for Service Level calculation.
    """
    _name = 'project.sla.control'
    _description = 'SLA Control Registry'

    doc_id = fields.Integer('Document ID', readonly=True)
    doc_model = fields.Char('Document Model', size=128, readonly=True)
    sla_line_id = fields.Many2one(
        'project.sla.line', 'Service Agreement')
    sla_warn_date = fields.Datetime('Warning Date')
    sla_limit_date = fields.Datetime('Limit Date')
    sla_start_date = fields.Datetime('Start Date')
    sla_close_date = fields.Datetime('Close Date')
    sla_achieved = fields.Integer('Achieved?')
    sla_state = fields.Selection(SLA_STATES, string="SLA Status")
    locked = fields.Boolean(
        'Recalculation disabled',
        help="Safeguard manual changes from future automatic "
                "recomputations.")
    
    def write(self, vals):
        """
        Update the related Document's SLA State when any of the SLA Control
        lines changes state
        """
        res = super().write(vals)
        new_state = vals.get('sla_state')
        if new_state:
            # just update sla_state without recomputing the whole thing
            ctx = dict(self._context) if self._context else {}
            ctx['__sla_stored__'] = 1
            for sla in self:
                doc = self.env[sla.doc_model].browse(sla.doc_id)
                if doc.sla_state < new_state:
                    doc.with_context(ctx).write({'sla_state': new_state})
        return res

    def update_sla_states(self):
        """
        Updates SLA States, given the current datetime:
        Only works on "open" sla states (watching, warning and will fail):
          - exceeded limit date are set to "will fail"
          - exceeded warning dates are set to "warning"
        To be used by a scheduled job.
        """
        now = dt.strftime(dt.now(), DT_FMT)
        # SLAs to mark as "will fail"
        control_objs = self.search(
            [('sla_state', 'in', ['2', '3']), ('sla_limit_date', '<', now)])
        control_objs.write({'sla_state': '4'})
        # SLAs to mark as "warning"
        control_objs = self.search(
            [('sla_state', 'in', ['2']), ('sla_warn_date', '<', now)])
        control_objs.write({'sla_state': '3'})
        return True

    def _compute_sla_date(self, calendar_id, resource_id,
                          start_date, hours):
        """
        Return a limit datetime by adding hours to a start_date, honoring
        a working_time calendar and a resource's (res_uid) timezone and
        availability (leaves)
        """
        # import pdb; pdb.set_trace()
        assert isinstance(start_date, dt)
        assert isinstance(hours, float) and hours >= 0

        cal_obj = self.env['resource.calendar'].browse(calendar_id)
        # resource = self.env['resource.resource'].browse(resource_id)
        resource = False
        # periods = cal_obj._schedule_hours(
        #     cr, uid, calendar_id,
        #     hours,
        #     day_dt=start_date,
        #     compute_leaves=True,
        #     resource_id=resource_id,
        #     default_interval=(8, 16),
        #     context=context)
        # end_date = periods[-1][1]
        date_end = cal_obj.plan_hours(
            hours,
            day_dt=start_date,
            compute_leaves=True,
            resource=resource)
        end_date = date_end
        return end_date
    
    @api.model
    def _get_computed_slas(self, doc):
        """
        Returns a dict with the computed data for SLAs, given a browse record
        for the target document.

        * The SLA used is either from a related analytic_account_id or
          project_id, whatever is found first.
        * The work calendar is taken from the Project's definitions ("Other
          Info" tab -> Working Time).
        * The timezone used for the working time calculations are from the
          document's responsible User (user_id) or from the current User (uid).

        For the SLA Achieved calculation:

        * Creation date is used to start counting time
        * Control date, used to calculate SLA achievement, is defined in the
          SLA Definition rules.
        """
        def datetime2str(dt_value, fmt):  # tolerant datetime to string
            return dt_value and dt.strftime(dt_value, fmt) or None

        res = []
        # sla_ids = (safe_getattr(doc, 'analytic_account_id.sla_ids') or
        #            safe_getattr(doc, 'project_id.analytic_account_id.sla_ids'))
        sla_ids = (safe_getattr(doc, 'contract_id.sla_ids'))
        if not sla_ids:
            return res
        cal_id = safe_getattr(doc, 'project_id.resource_calendar_id')
        if not cal_id:
            _logger.debug('Project %s has no calendar!', doc.project_id.name)
            return []
        if not cal_id.attendance_ids:
            _logger.debug('Calendar %s has no work periods!', cal_id.name)
            return []

        for sla in sla_ids:
            if sla.control_model != doc._name:
                continue  # SLA not for this model; skip

            for l in sla.sla_line_ids:
                eval_context = {'o': doc, 'obj': doc, 'object': doc}
                if not l.condition or safe_eval(l.condition, eval_context):
                    # start_date = dt.strptime(doc.fecha_incidencia, DT_FMT)
                    start_date = doc.issue_date
                    res_uid = doc.user_id.id or self._uid
                    cal = safe_getattr(
                        doc, 'project_id.resource_calendar_id.id')
                    warn_date = self._compute_sla_date(cal, res_uid,
                        start_date, l.warn_qty)
                    lim_date = self._compute_sla_date(cal, res_uid,
                        warn_date, l.limit_qty - l.warn_qty)
                    # evaluate sla state
                    control_val = getattr(doc, sla.control_field_id.name)
                    if control_val:
                        # control_date = dt.strptime(control_val, DT_FMT)
                        control_date = control_val
                        if control_date > lim_date:
                            sla_val, sla_state = 0, '5'  # failed
                        else:
                            sla_val, sla_state = 1, '1'  # achieved
                    else:
                        control_date = None
                        now = dt.now()
                        if now > lim_date:
                            sla_val, sla_state = 0, '4'  # will fail
                        elif now > warn_date:
                            sla_val, sla_state = 0, '3'  # warning
                        else:
                            sla_val, sla_state = 0, '2'  # watching

                    res.append(
                        {'sla_line_id': l.id,
                         'sla_achieved': sla_val,
                         'sla_state': sla_state,
                         'sla_warn_date': datetime2str(warn_date, DT_FMT),
                         'sla_limit_date': datetime2str(lim_date, DT_FMT),
                         'sla_start_date': datetime2str(start_date, DT_FMT),
                         'sla_close_date': datetime2str(control_date, DT_FMT),
                         'doc_id': doc.id,
                         'doc_model': sla.control_model})
                    break

        if sla_ids and not res:
            _logger.warning("No valid SLA rule foun for %d, SLA Ids %s",
                            doc.id, repr([x.id for x in sla_ids]))
        return res
    
    @api.model
    def store_sla_control(self, docs):
        """
        Used by controlled documents to ask for SLA calculation and storage.
        ``docs`` is a Browse object
        """
        # import ipdb; ipdb.set_trace()
        # context flag to avoid infinite loops on further writes
        context = self._context or {}
        if '__sla_stored__' in self._context:
            return False
        else:
            ctx = dict(context)
            ctx['__sla_stored__'] = 1

        res = []
        for ix, doc in enumerate(docs):
            if ix and ix % 50 == 0:
                _logger.info('...%d SLAs recomputed for %s', ix, doc._name)
            control = {x.sla_line_id.id: x
                       for x in doc.sla_control_ids}
            sla_recs = self.with_context(ctx)._get_computed_slas(doc)
            # calc sla control lines
            if sla_recs:
                slas = []
                for sla_rec in sla_recs:
                    sla_line_id = sla_rec.get('sla_line_id')
                    if sla_line_id in control:
                        control_rec = control.get(sla_line_id)
                        if not control_rec.locked:
                            slas += m2m.write(control_rec.id, sla_rec)
                    else:
                        slas += m2m.add(sla_rec)
                global_sla = max([sla[2].get('sla_state') for sla in slas])
            else:
                slas = m2m.clear()
                global_sla = None
            # calc sla control summary and store
            vals = {'sla_state': global_sla, 'sla_control_ids': slas}

            # regular users can't write on SLA Control
            doc.with_context(ctx).sudo().write(vals)
        return res


class SLAControlled(models.AbstractModel):
    """
    SLA Controlled documents: AbstractModel to apply SLA control on Models
    """
    _name = 'project.sla.controlled'
    _description = 'SLA Controlled Document'

    sla_control_ids = fields.Many2many(
        'project.sla.control', string="SLA Control", ondelete='cascade')
    sla_state = fields.Selection(
        SLA_STATES, string="SLA Status", readonly=True)

    @api.model
    def create(self, vals):
        res = super().create(vals)
        docs = res
        self.env['project.sla.control'].store_sla_control(docs)
        return res

    def write(self, vals):
        res = super().write(vals)
        docs = self.filtered(
            lambda x: not x.stage_id.fold or x.sla_state not in ['1', '5'])
        self.env['project.sla.control'].store_sla_control(docs)
        return res

    def unlink(self):
        # Unlink and delete all related Control records
        for doc in self:
            vals = [m2m.remove(x.id)[0] for x in doc.sla_control_ids]
            doc.write({'sla_control_ids': vals})
        return super().unlink()



    