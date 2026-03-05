# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Nmbrs (HR)",
    "summary": "HR integration for Nmbrs",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Localization",
    "website": "https://github.com/OCA/l10n-netherlands",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "depends": [
        "nmbrs_base",
        "hr",
    ],
    "auto_install": True,
    "data": [
        "data/ir_actions_server.xml",
        "views/hr_employee.xml",
    ],
}
