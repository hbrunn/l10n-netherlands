# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.nmbrs_base.helpers import raise_nmbrs_error


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    nmbrs_id = fields.Integer(
        "Nmbrs ID", help="If empty, this employee has not been pushed to Nmbrs yet"
    )
    nmbrs_company_id = fields.Many2one(
        "nmbrs.company", string="Company (Nmbrs)", help="Leave empty for default"
    )
    nmbrs_start_date = fields.Date("Start date")

    def _nmbrs_hr_push(self, client=None):
        self._nmbrs_hr_push_validate()
        client = client or self.company_id._nmbrs_base_get_client("EmployeeService")
        for this in self:
            if not this.nmbrs_id:
                with raise_nmbrs_error():
                    this.nmbrs_id = client.service.Employee_Insert(
                        **this._nmbrs_hr_to_employee_insert_kwargs()
                    )
            with raise_nmbrs_error():
                client.service.PersonalInfo_UpdateCurrent(
                    EmployeeId=this.nmbrs_id,
                    PersonalInfo=this._nmbrs_hr_to_personal_info(),
                )

    def _nmbrs_hr_push_validate(self):
        if not all(self.mapped("nmbrs_start_date")):
            raise UserError(_("Start date is mandatory for push to Nmbrs"))

    def _nmbrs_hr_to_employee_insert_kwargs(self):
        name_splits = self.name.split()
        first_name = " ".join(name_splits[:-1]) if len(name_splits) > 1 else ""
        last_name = " ".join(name_splits[-1:])
        result = {
            "StartDate": self.nmbrs_start_date,
            "FirstName": self.firstname if "firstname" in self._fields else first_name,
            "LastName": self.lastname if "lastname" in self._fields else last_name,
            "CompanyId": self.nmbrs_company_id.nmbrs_id
            or self.env["nmbrs.company"]._nmbrs_default(self).nmbrs_id,
            "UnprotectedMode": self.env.user.has_group("nmbrs_base.group_manager"),
        }
        return result

    def _nmbrs_hr_to_personal_info(self):
        insert_kwargs = self._nmbrs_hr_to_employee_insert_kwargs()
        result = {
            "Id": self.nmbrs_id,
            "Number": self.id,
            "EmployeeNumber": self.id,
            "FirstName": insert_kwargs["FirstName"],
            "LastName": insert_kwargs["LastName"],
            "Nickname": insert_kwargs["FirstName"],
            "EmailWork": self.work_email or None,
            "NationalityCode": self.country_id.nmbrs_code or "1",
            "BurgerlijkeStaat": {
                "married": "Gehuwd",
                "single": "Ongehuwd",
                "cohabitant": "Samenwonend",
                "divorced": "Duurz. Gescheiden",
                "widower": "Weduwe/Weduwnaar",
            }.get(self.marital, "-"),
            "Gender": self.gender if self.gender in ("male", "female") else "unknown",
            "TelephoneMobileWork": self.mobile_phone or None,
            "TelephoneWork": self.work_phone or None,
            "Birthday": self.birthday or None,
            "IdentificationType": "10"
            if self.identification_id
            else "1"
            if self.passport_id
            else "0",
            "IdentificationNumber": self.identification_id or self.passport_id or None,
            "CountryOfBirthISOCode": self.country_of_birth.code or None,
            "PlaceOfBirth": self.place_of_birth or None,
        }
        return result
