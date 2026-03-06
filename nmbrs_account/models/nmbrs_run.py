# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import datetime

from lxml import etree

from odoo import fields, models


def xpath_text(node, xpath):
    found = node.xpath(xpath)
    return found[0].text if found else ""


class NmbrsRun(models.Model):
    _inherit = "nmbrs.record.mixin"
    _name = "nmbrs.run"
    _description = "A run in Nmbrs"
    _order = "nmbrs_number desc"

    name = fields.Char(
        required=True, nmbrs_name="Description", nmbrs_create=True, nmbrs_update=True
    )
    nmbrs_id = fields.Integer(
        "Nmbrs ID", nmbrs_name="ID", nmbrs_create=True, nmbrs_find=True, required=True
    )
    nmbrs_number = fields.Integer(
        "Number", nmbrs_name="Number", nmbrs_create=True, required=True
    )
    nmbrs_year = fields.Integer("Year", nmbrs_name="Year", nmbrs_create=True)
    nmbrs_period_start = fields.Integer(
        "Period Start", nmbrs_name="PeriodStart", nmbrs_create=True
    )
    nmbrs_period_end = fields.Integer(
        "Period End", nmbrs_name="PeriodEnd", nmbrs_create=True
    )
    nmbrs_run_at = fields.Date("Run at", nmbrs_name="RunAt", nmbrs_create=True)
    nmbrs_is_locked = fields.Boolean(
        "Locked", nmbrs_name="IsLocked", nmbrs_create=True, nmbrs_update=True
    )
    nmbrs_company_id = fields.Many2one(
        "nmbrs.company",
        string="Company (Nmbrs)",
        required=True,
        ondelete="cascade",
    )
    move_id = fields.Many2one("account.move", string="Journal Entry")
    company_id = fields.Many2one(related="nmbrs_company_id.company_id")

    def _create_from_nmbrs(self, record, nmbrs_company):
        return super()._create_from_nmbrs(record, nmbrs_company_id=nmbrs_company.id)

    def action_import_move(self, client=None):
        client = client or self.company_id._nmbrs_base_get_client("CompanyService")
        journal_xml = client.service.Journals_GetByRunCompany(
            CompanyId=self.nmbrs_company_id.nmbrs_id, RunId=self.nmbrs_id
        )
        journal_doc = etree.fromstring(journal_xml)
        move_vals_list = []
        for transaction_node in journal_doc:
            date = datetime.datetime.strptime(
                xpath_text(transaction_node, "./header/date"),
                "%Y%m%d",
            )
            move_vals = {
                "date": date,
                "line_ids": [],
                "company_id": self.company_id.id,
            }
            move_vals_list.append(move_vals)
            for line in transaction_node.xpath("./lines/line"):
                line_vals = self._import_move_line_vals(line)
                move_vals["line_ids"].append(fields.Command.create(line_vals))

        self.move_id = self._import_move_create_move(move_vals_list)
        self.move_id.action_post()

    def _import_move_line_vals(self, line_node):
        analytic_account = self.env["account.analytic.account"]._find_from_nmbrs_code(
            xpath_text(line_node, "./dim1 | ./dim2 | ./dim3"),
            self,
            line_node,
        )
        return {
            "name": xpath_text(line_node, "./description"),
            "account_id": self.env["account.account"]
            ._find_from_nmbrs_code(
                xpath_text(line_node, "./dim1"),
                self,
                line_node,
            )
            .id,
            "analytic_distribution": {
                analytic_account.id: 100,
            }
            if analytic_account
            else None,
            "credit": float(xpath_text(line_node, "./value"))
            if xpath_text(line_node, "./debitcredit") == "credit"
            else 0,
            "debit": float(xpath_text(line_node, "./value"))
            if xpath_text(line_node, "./debitcredit") == "debit"
            else 0,
        }

    def _import_move_create_move(self, move_vals_list):
        return self.env["account.move"].create(move_vals_list)
