# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Nmbrs (Accounting)",
    "summary": "Accounting integration for Nmbrs",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Localization",
    "website": "https://github.com/OCA/l10n-netherlands",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "depends": [
        "nmbrs_base",
        "account",
    ],
    "auto_install": True,
    "data": [
        "views/menu.xml",
        "views/account_account.xml",
        "views/account_analytic_account.xml",
        "views/nmbrs_company.xml",
        "wizards/nmbrs_run_import_wizard.xml",
        "security/ir.model.access.csv",
        "security/nmbrs_account.xml",
    ],
}
