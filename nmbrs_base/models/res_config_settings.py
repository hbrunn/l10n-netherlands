# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    nmbrs_base_api_domain = fields.Char(
        related="company_id.nmbrs_base_api_domain", readonly=False
    )
    nmbrs_base_api_username = fields.Char(
        related="company_id.nmbrs_base_api_username", readonly=False
    )
    nmbrs_base_api_key = fields.Char(
        related="company_id.nmbrs_base_api_key", readonly=False
    )
    nmbrs_base_api_sandbox = fields.Boolean(
        related="company_id.nmbrs_base_api_sandbox", readonly=False
    )

    def action_nmbrs_base_fetch_master_data(self):
        return self.company_id.action_nmbrs_base_fetch_master_data()
