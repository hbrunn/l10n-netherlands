# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class NmbrsRecordMixin(models.AbstractModel):
    _name = "nmbrs.record.mixin"
    _description = "Mixin for Odoo records mirroring Nmbrs records"

    def _valid_field_parameter(self, field, name):
        return super()._valid_field_parameter(field, name) or name in (
            "nmbrs_name",
            "nmbrs_create",
            "nmbrs_update",
            "nmbrs_find",
        )

    def _find_from_nmbrs(self, record):
        return self.search(
            [
                (field_name, "=", record[field.nmbrs_name])
                for field_name, field in self._fields.items()
                if field.args.get("nmbrs_find")
            ]
        )

    def _update_from_nmbrs(self, record):
        self.write(
            {
                field_name: record[field.nmbrs_name]
                for field_name, field in self._fields.items()
                if field.args.get("nmbrs_update")
            }
        )

    def _create_from_nmbrs(self, record, **extra_args):
        return self.create(
            dict(
                {
                    field_name: record[field.nmbrs_name]
                    for field_name, field in self._fields.items()
                    if field.args.get("nmbrs_create")
                },
                **extra_args
            )
        )
