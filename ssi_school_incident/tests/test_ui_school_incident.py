# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. See structure-and-runner.md "Base class".
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolIncident(HttpSavepointCase):
    """Tour tests for the ``school_incident`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant the menu group and build fixtures for the three tours.

        Pre-Condition: this menu is gated by ``school_incident_user_
        group``. Without it the tour dies on its FIRST step -- the menu
        is never rendered. The Confirm and Approve tours also need one
        pre-existing ``school_incident`` record each, in Draft and
        Waiting for Approval respectively, identified in the list by a
        unique Student name.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        group = cls.env.ref("ssi_school_incident.school_incident_user_group")
        group.sudo().write({"users": [(4, cls.admin.id)]})

        incident_type = cls.env.ref("ssi_school_incident.school_incident_type_academic")
        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Grade Type for Incident UI Test",
                "code": "GTINCUI",
                "sequence": 10,
            }
        )
        school = cls.env["school"].create(
            {
                "name": "School for Incident UI Test",
                "code": "SCHINCUI",
                "grade_type_id": grade_type.id,
            }
        )

        def _make_student(name, code):
            """Create a ``school_student`` fixture with its own contact.

            :param name: student name, used as the list-row marker
            :param code: unique student code
            :return: the created ``school_student`` record
            """
            contact = cls.env["res.partner"].create({"name": name + " Contact"})
            return cls.env["school_student"].create(
                {
                    "name": name,
                    "code": code,
                    "contact_id": contact.id,
                    "school_id": school.id,
                }
            )

        # Flow 1 (Create) picks this student by name via the autocomplete.
        _make_student("Tour Incident Student", "TOURINC01")

        student_confirm = _make_student("Student For Confirm Tour", "TOURINC02")
        cls.incident_confirm = cls.env["school_incident"].create(
            {
                "student_id": student_confirm.id,
                "incident_type_id": incident_type.id,
                "description": "Fixture incident used by the Confirm tour.",
            }
        )

        student_approve = _make_student("Student For Approve Tour", "TOURINC03")
        cls.incident_approve = cls.env["school_incident"].create(
            {
                "student_id": student_approve.id,
                "incident_type_id": incident_type.id,
                "description": "Fixture incident used by the Approve tour.",
            }
        )
        cls.incident_approve.with_user(cls.admin).action_confirm()
        cls.incident_approve.invalidate_cache()

    def test_create(self):
        """Run the create tour for ``school_incident``.

        IK: docs/school_incident/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_incident_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_incident``.

        IK: docs/school_incident/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_incident_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_incident``.

        IK: docs/school_incident/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_incident_approve",
            login="admin",
        )
