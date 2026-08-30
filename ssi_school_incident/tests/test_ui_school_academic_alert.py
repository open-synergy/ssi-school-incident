# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. See structure-and-runner.md "Base class".
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolAcademicAlert(HttpSavepointCase):
    """Tour tests for the ``school_academic_alert`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant the menu/approval groups and build fixtures for the tours.

        Pre-Condition: the Academic Alerts menu is gated by
        ``school_incident_user_group`` (``views/school_academic_alert.
        xml``), not by a group named after this model. Without it the
        tour dies on its FIRST step -- the menu is never rendered.
        Approve additionally needs ``school_incident_officer_group``:
        that is the approver group configured in ``approval_template/
        school_academic_alert.xml``, so without it ``approve_ok`` stays
        False and the Approve button never appears. Cancel needs
        ``school_academic_alert_validator_group`` (``policy_template/
        school_academic_alert.xml``). The Confirm, Approve, Finish, and
        Cancel tours also need one pre-existing ``school_academic_alert``
        record each, in the state each tour starts from, identified in
        the list by a unique Student name.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        group = cls.env.ref("ssi_school_incident.school_incident_user_group")
        group.sudo().write({"users": [(4, cls.admin.id)]})
        officer_group = cls.env.ref("ssi_school_incident.school_incident_officer_group")
        officer_group.sudo().write({"users": [(4, cls.admin.id)]})
        validator_group = cls.env.ref(
            "ssi_school_incident.school_academic_alert_validator_group"
        )
        validator_group.sudo().write({"users": [(4, cls.admin.id)]})

        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Grade Type for Academic Alert UI Test",
                "code": "GTALERTUI",
                "sequence": 10,
            }
        )
        school = cls.env["school"].create(
            {
                "name": "School for Academic Alert UI Test",
                "code": "SCHALERTUI",
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
        _make_student("Tour Academic Alert Student", "TOURALT01")

        student_confirm = _make_student("Student For Alert Confirm Tour", "TOURALT02")
        cls.alert_confirm = cls.env["school_academic_alert"].create(
            {
                "student_id": student_confirm.id,
                "subject_note": "Confirm tour fixture",
            }
        )

        student_approve = _make_student("Student For Alert Approve Tour", "TOURALT03")
        cls.alert_approve = cls.env["school_academic_alert"].create(
            {
                "student_id": student_approve.id,
                "subject_note": "Approve tour fixture",
            }
        )
        cls.alert_approve.with_user(cls.admin).action_confirm()
        cls.alert_approve.invalidate_cache()

        # Pre-Condition for 09-finish -- Open (confirmed and approved),
        # same recipe as alert_approve above plus the approve step
        # itself. invalidate_cache() between the two calls avoids the
        # stale-policy-cache trap when action_approve_approval() reads
        # approve_ok right after action_confirm() wrote confirm_ok in
        # the same environment (T-04).
        student_finish = _make_student("Student For Alert Finish Tour", "TOURALT04")
        cls.alert_finish = cls.env["school_academic_alert"].create(
            {
                "student_id": student_finish.id,
                "subject_note": "Finish tour fixture",
            }
        )
        cls.alert_finish.with_user(cls.admin).action_confirm()
        cls.alert_finish.invalidate_cache()
        cls.alert_finish.with_user(cls.admin).action_approve_approval()
        cls.alert_finish.invalidate_cache()

        # Pre-Condition for 10-cancel -- a Draft alert, plus the
        # Cancellation Reason the wizard requires.
        student_cancel = _make_student("Student For Alert Cancel Tour", "TOURALT05")
        cls.alert_cancel = cls.env["school_academic_alert"].create(
            {
                "student_id": student_cancel.id,
                "subject_note": "Cancel tour fixture",
            }
        )
        cls.env["base.cancel_reason"].create(
            {
                "name": "Tour Academic Alert Cancel Reason",
                "code": "TOURALTCR",
                # The cancel wizard's radio widget only lists reasons in
                # ir.model.all_cancel_reason_ids, which merges
                # model-specific links with every global_use=True
                # reason. Without this, the tour's radio option never
                # renders.
                "global_use": True,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_academic_alert``.

        IK: docs/school_academic_alert/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_academic_alert_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_academic_alert``.

        IK: docs/school_academic_alert/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_academic_alert_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_academic_alert``.

        IK: docs/school_academic_alert/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_academic_alert_approve",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``school_academic_alert``.

        IK: docs/school_academic_alert/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_academic_alert_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_academic_alert``.

        IK: docs/school_academic_alert/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_academic_alert_cancel",
            login="admin",
        )
