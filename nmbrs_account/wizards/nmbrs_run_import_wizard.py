# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class NmbrsRunImportWizard(models.TransientModel):
    _name = "nmbrs.run.import.wizard"
    _description = "Import payroll runs from Nmbrs"

    nmbrs_company_id = fields.Many2one("nmbrs.company")
    year = fields.Integer(default=lambda self: fields.Date.today().year)

    def action_import(self, client=None):
        client = client or self.nmbrs_company_id.company_id._nmbrs_base_get_client(
            "CompanyService"
        )
        NmbrsRun = self.env["nmbrs.run"]
        for run in (
            client.service.Run_GetList(
                CompanyId=self.nmbrs_company_id.nmbrs_id, Year=self.year
            )
            or []
        ):
            existing = NmbrsRun._find_from_nmbrs(run)
            if existing:
                existing._update_from_nmbrs(run)
            else:
                NmbrsRun._create_from_nmbrs(run, self.nmbrs_company_id)
