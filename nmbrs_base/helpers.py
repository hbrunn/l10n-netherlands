# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from contextlib import contextmanager

import zeep

from odoo.exceptions import UserError


@contextmanager
def raise_nmbrs_error():
    try:
        yield
    except zeep.exceptions.Fault as server_fault:
        raise UserError(server_fault) from server_fault
