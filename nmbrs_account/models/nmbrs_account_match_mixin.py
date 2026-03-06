# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models
from odoo.osv.expression import AND


class NmbrsAccountMatchMixin(models.AbstractModel):
    _name = "nmbrs.account.match.mixin"
    _description = "A mixin to match account to Nmbrs account"

    nmbrs_code = fields.Char(
        help="Fill in the code(s) of Nmbrs accounts you want to match with this account."
        " Separate with spaces"
    )

    def _find_from_nmbrs_code(
        self, code, nmbrs_record, journal_line_node, extra_domain=None
    ):
        extra_domain = AND(
            (extra_domain or [], [("company_id", "=", nmbrs_record.company_id.id)])
        )
        return (
            self.search(
                AND(([("nmbrs_code", "=", code)], extra_domain)),
                limit=1,
            )
            or self.search(
                AND(
                    (
                        [
                            "|",
                            "|",
                            ("nmbrs_code", "like", f"{code} %"),
                            ("nmbrs_code", "like", f"% {code}"),
                            ("nmbrs_code", "like", f"% {code} %"),
                        ],
                        extra_domain,
                    )
                ),
                limit=1,
            )
            or self.search(AND(([("code", "=", code)], extra_domain)))
        )
