# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class ResCompany(models.Model):
    _inherit = ["res.company", "nmbrs_base.config_mixin"]
    _name = "res.company"

    def action_nmbrs_base_fetch_master_data(self):
        self = self.with_context(default_company_id=self.id)
        return super().action_nmbrs_base_fetch_master_data()
