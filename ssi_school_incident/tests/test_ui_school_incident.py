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
        """Grant the menu groups and build fixtures for the five tours.

        Pre-Condition: this menu is gated by ``school_incident_user_
        group``. Without it the tour dies on its FIRST step -- the menu
        is never rendered. Cancel additionally requires
        ``school_incident_officer_group`` (``policy_template/
        school_incident.xml``: the ``cancel`` policy detail is gated on
        that group, one tier above ``user``). The Confirm, Approve,
        Finish, and Cancel tours also need one pre-existing
        ``school_incident`` record each, in the state each tour starts
        from, identified in the list by a unique Student name.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        group = cls.env.ref("ssi_school_incident.school_incident_user_group")
        group.sudo().write({"users": [(4, cls.admin.id)]})
        officer_group = cls.env.ref("ssi_school_incident.school_incident_officer_group")
        officer_group.sudo().write({"users": [(4, cls.admin.id)]})

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

        # Pre-Condition for 09-finish -- Open (confirmed and approved),
        # same recipe as incident_approve above plus the approve step
        # itself. invalidate_cache() between the two calls avoids the
        # stale-policy-cache trap when action_approve_approval() reads
        # approve_ok right after action_confirm() wrote confirm_ok in
        # the same environment (T-04).
        student_finish = _make_student("Student For Finish Tour", "TOURINC04")
        cls.incident_finish = cls.env["school_incident"].create(
            {
                "student_id": student_finish.id,
                "incident_type_id": incident_type.id,
                "description": "Fixture incident used by the Finish tour.",
            }
        )
        cls.incident_finish.with_user(cls.admin).action_confirm()
        cls.incident_finish.invalidate_cache()
        cls.incident_finish.with_user(cls.admin).action_approve_approval()
        cls.incident_finish.invalidate_cache()

        # Pre-Condition for 10-cancel -- a Draft incident, plus the
        # Cancellation Reason the wizard requires.
        student_cancel = _make_student("Student For Cancel Tour", "TOURINC05")
        cls.incident_cancel = cls.env["school_incident"].create(
            {
                "student_id": student_cancel.id,
                "incident_type_id": incident_type.id,
                "description": "Fixture incident used by the Cancel tour.",
            }
        )
        cls.env["base.cancel_reason"].create(
            {
                "name": "Tour Cancel Reason",
                "code": "TOURINCCR",
                # The cancel wizard's radio widget only lists reasons in
                # ir.model.all_cancel_reason_ids, which merges
                # model-specific links with every global_use=True
                # reason. Without this, the tour's radio option never
                # renders.
                "global_use": True,
            }
        )

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

    def test_finish(self):
        """Run the finish tour for ``school_incident``.

        IK: docs/school_incident/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_incident_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_incident``.

        IK: docs/school_incident/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_incident_cancel",
            login="admin",
        )
