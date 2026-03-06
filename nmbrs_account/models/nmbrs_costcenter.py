# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class NmbrsCostcenter(models.Model):
    _name = "nmbrs.costcenter"
    _description = "A costcenter in Nmbrs"
    _order = "nmbrs_code"

    name = fields.Char(required=True)
    nmbrs_id = fields.Integer("Nmbrs ID", required=True)
    nmbrs_code = fields.Char("Code", required=True)
    nmbrs_company_id = fields.Many2one(
        "nmbrs.company",
        string="Company (Nmbrs)",
        required=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(related="nmbrs_company_id.company_id")

    def _find_from_nmbrs(self, costcenter):
        return self.search([("nmbrs_id", "=", costcenter["Id"])])

    def _update_from_nmbrs(self, costcenter):
        self.write(
            {
                "name": costcenter["Description"],
                "nmbrs_code": costcenter["Code"],
            }
        )

    def _create_from_nmbrs(self, costcenter, nmbrs_company):
        return self.create(
            {
                "nmbrs_id": costcenter["Id"],
                "name": costcenter["Description"],
                "nmbrs_code": costcenter["Code"],
                "nmbrs_company_id": nmbrs_company.id,
            }
        )
