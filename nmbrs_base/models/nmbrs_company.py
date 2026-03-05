# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class NmbrsComany(models.Model):
    _name = "nmbrs.company"
    _description = "A company in Nmbrs"

    nmbrs_id = fields.Integer(string="Nmbrs ID", required=True)
    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company")

    def _find_from_nmbrs(self, company):
        return self.search([("nmbrs_id", "=", company["ID"])])

    def _update_from_nmbrs(self, company):
        self.write(
            {
                "name": company["Name"],
            }
        )

    def _create_from_nmbrs(self, company):
        return self.create(
            {
                "nmbrs_id": company["ID"],
                "name": company["Name"],
            }
        )

    def _nmbrs_default(self, record):
        domain = []
        if "company_id" in record._fields:
            domain += [("company_id", "=", record.company_id.id)]
        return self.search(domain, limit=1)
