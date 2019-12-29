# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields


class ProjectSla(models.Model):
    _name = 'project.sla'

    name =  fields.Char('Title', size=64, required=True, translate=True)
    active =  fields.Boolean('Active', default=True)
    control_model =  fields.Char('For documents', size=128, required=True)
    control_field_id =  fields.Many2one(
        'ir.model.fields', 'Control Date', required=True,
        domain="[('model_id.model', '=', control_model),"
                " ('ttype', 'in', ['date', 'datetime'])]",
        help="Date field used to check if the SLA was achieved.")
    sla_line_ids =  fields.One2many(
        'project.sla.line', 'sla_id', 'Definitions', copy=True)
    contract_ids =  fields.Many2many(
        'contract.contract', string='Contracts')
    

class SlaRules(models.Model):
    _name = 'project.sla.line'
    _order = 'sla_id, sequence'

    sla_id =  fields.Many2one('project.sla', 'SLA Definition')
    sequence =  fields.Integer('Sequence', default=10)
    name =  fields.Char('Title', size=64, required=True, translate=True)
    condition =  fields.Char(
        'Condition', size=256, help="Apply only if this expression is "
        "evaluated to True. The document fields can be accessed using "
        "either o, obj or object. Example: obj.priority <= '2'")
    limit_qty =  fields.Float('Hours to Limit')
    warn_qty =  fields.Float('Hours to Warn')




   