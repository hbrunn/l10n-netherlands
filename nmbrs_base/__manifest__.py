# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Nmbrs",
    "summary": "Base for Nmbrs integration in Odoo",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Localization",
    "website": "https://github.com/OCA/l10n-netherlands",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "depends": [
        "base_setup",
    ],
    "data": [
        "data/res_country.xml",
        "security/nmbrs_base.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings.xml",
        "views/nmbrs_company.xml",
    ],
    "external_dependencies": {
        "python": [
            "zeep",
        ],
    },
}
