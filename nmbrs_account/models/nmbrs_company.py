# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class NmbrsCompany(models.Model):
    _inherit = "nmbrs.company"

    nmbrs_costcenter_ids = fields.One2many(
        "nmbrs.costcenter", "nmbrs_company_id", string="Costcenters"
    )
    nmbrs_run_ids = fields.One2many(
        "nmbrs.run", "nmbrs_company_id", string="Payroll runs"
    )

    def action_nmbrs_run_import_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "nmbrs.run.import.wizard",
            "target": "new",
            "context": {
                "default_nmbrs_company_id": self.id,
            },
            "views": [(False, "form")],
        }
