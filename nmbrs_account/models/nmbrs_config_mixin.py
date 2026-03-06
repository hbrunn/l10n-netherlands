# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class NmbrsConfigMixin(models.AbstractModel):
    _inherit = "nmbrs.config.mixin"

    def _action_nmbrs_base_fetch_master_data(self):
        nmbrs_companies = super()._action_nmbrs_base_fetch_master_data()

        client = self._nmbrs_base_get_client("CompanyService")
        NmbrsCostcenter = self.env["nmbrs.costcenter"]
        for nmbrs_company in nmbrs_companies:
            for costcenter in (
                client.service.CostCenter_GetList(nmbrs_company.nmbrs_id) or []
            ):
                existing = NmbrsCostcenter._find_from_nmbrs(costcenter)
                if existing:
                    existing._update_from_nmbrs(costcenter)
                else:
                    NmbrsCostcenter._create_from_nmbrs(costcenter, nmbrs_company)

        return nmbrs_companies
