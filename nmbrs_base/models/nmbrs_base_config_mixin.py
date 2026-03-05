# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import zeep

from odoo import _, fields, models

from ..helpers import raise_nmbrs_error


class NmbrsBaseConfigMixin(models.AbstractModel):
    _name = "nmbrs_base.config_mixin"
    _description = "Mixin for models needing a Nmbrs configuration"

    nmbrs_base_api_domain = fields.Char("Domain", groups="nmbrs_base.group_manager")
    nmbrs_base_api_username = fields.Char(
        "Username (email)", groups="nmbrs_base.group_manager"
    )
    nmbrs_base_api_key = fields.Char(
        "API key (token)", groups="nmbrs_base.group_manager"
    )
    nmbrs_base_api_sandbox = fields.Boolean(
        "Use sandbox", groups="nmbrs_base.group_manager", default=True
    )

    def _nmbrs_base_get_client(self, service):
        self.ensure_one()
        cache_key = (self._name, self._nmbrs_base_get_client.__func__, self.id, service)
        cached = self.env.registry._Registry__cache.get(cache_key)
        if cached:
            return cached
        api_host = (
            "api-sandbox.nmbrs.nl" if self.nmbrs_base_api_sandbox else "api.nmbrs.nl"
        )
        # flake8 misunderstands the colon in the f-string
        client = zeep.Client(
            f"https://{api_host}/soap/v3/{service}.asmx?WSDL"  # noqa: E231
        )
        client.set_default_soapheaders(
            {
                "AuthHeaderWithDomain": {
                    "Username": self.nmbrs_base_api_username,
                    "Token": self.nmbrs_base_api_key,
                    "Domain": self.nmbrs_base_api_domain,
                }
            }
        )
        self.env.registry._Registry__cache[cache_key] = client
        return client

    def action_nmbrs_base_fetch_master_data(self):
        client = self._nmbrs_base_get_client("CompanyService")
        with raise_nmbrs_error():
            companies = client.service.List_GetAll()
        NmbrsCompany = self.env["nmbrs.company"]
        records = NmbrsCompany.browse([])
        for company in companies:
            existing = NmbrsCompany._find_from_nmbrs(company)
            if existing:
                existing._update_from_nmbrs(company)
                records += existing
            else:
                records += NmbrsCompany._create_from_nmbrs(company)

        return {
            "type": "ir.actions.act_window",
            "name": _("Created/updated Nmbrs companies"),
            "res_model": "nmbrs.company",
            "views": [(False, "tree"), (False, "form")],
        }
