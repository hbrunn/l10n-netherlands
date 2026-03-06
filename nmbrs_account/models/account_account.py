# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class AccountAccount(models.Model):
    _inherit = ["account.account", "nmbrs.account.match.mixin"]
    _name = "account.account"
