# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. See structure-and-runner.md "Base class".
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolIncidentWeeklyReview(HttpSavepointCase):
    """Tour tests for the ``school_incident_weekly_review`` work
    instructions.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the menu/approval groups and build fixtures for the tours.

        Pre-Condition: the Weekly Case Reviews menu is gated by
        ``school_incident_officer_group`` (``views/school_incident_
        weekly_review.xml``), not by a group named after this model.
        Without it the tour dies on its FIRST step -- the menu is
        never rendered. Confirm additionally needs
        ``school_incident_weekly_review_user_group`` (``policy_
        template/school_incident_weekly_review.xml``). Approve needs
        ``school_incident_manager_group``: that is the approver group
        configured in ``approval_template/school_incident_weekly_
        review.xml``, so without it ``approve_ok`` stays False and the
        Approve button never appears. Cancel needs
        ``school_incident_weekly_review_validator_group``. The
        Confirm, Approve, and Cancel tours also need one pre-existing
        ``school_incident_weekly_review`` record each, in the state
        each tour starts from, identified in the list by a unique
        School name.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        officer_group = cls.env.ref("ssi_school_incident.school_incident_officer_group")
        officer_group.sudo().write({"users": [(4, cls.admin.id)]})
        review_user_group = cls.env.ref(
            "ssi_school_incident.school_incident_weekly_review_user_group"
        )
        review_user_group.sudo().write({"users": [(4, cls.admin.id)]})
        review_validator_group = cls.env.ref(
            "ssi_school_incident.school_incident_weekly_review_validator_group"
        )
        review_validator_group.sudo().write({"users": [(4, cls.admin.id)]})
        manager_group = cls.env.ref("ssi_school_incident.school_incident_manager_group")
        manager_group.sudo().write({"users": [(4, cls.admin.id)]})

        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "Grade Type for Weekly Review UI Test",
                "code": "GTWRUI",
                "sequence": 10,
            }
        )

        def _make_school(name, code):
            """Create a ``school`` fixture, used as the list-row marker.

            :param name: school name, used as the list-row marker
            :param code: unique school code
            :return: the created ``school`` record
            """
            return cls.env["school"].create(
                {
                    "name": name,
                    "code": code,
                    "grade_type_id": grade_type.id,
                }
            )

        school_confirm = _make_school(
            "School For Weekly Review Confirm Tour", "SCHWRCON"
        )
        cls.review_confirm = cls.env["school_incident_weekly_review"].create(
            {
                "school_id": school_confirm.id,
                "date_start": "2026-06-22",
                "date_end": "2026-06-26",
            }
        )

        school_approve = _make_school(
            "School For Weekly Review Approve Tour", "SCHWRAPP"
        )
        cls.review_approve = cls.env["school_incident_weekly_review"].create(
            {
                "school_id": school_approve.id,
                "date_start": "2026-06-22",
                "date_end": "2026-06-26",
            }
        )
        cls.review_approve.with_user(cls.admin).action_confirm()
        cls.review_approve.invalidate_cache()

        # Pre-Condition for 10-cancel -- a Draft review, plus the
        # Cancellation Reason the wizard requires.
        school_cancel = _make_school("School For Weekly Review Cancel Tour", "SCHWRCAN")
        cls.review_cancel = cls.env["school_incident_weekly_review"].create(
            {
                "school_id": school_cancel.id,
                "date_start": "2026-06-22",
                "date_end": "2026-06-26",
            }
        )
        cls.env["base.cancel_reason"].create(
            {
                "name": "Tour Weekly Review Cancel Reason",
                "code": "TOURWRCR",
                # The cancel wizard's radio widget only lists reasons in
                # ir.model.all_cancel_reason_ids, which merges
                # model-specific links with every global_use=True
                # reason. Without this, the tour's radio option never
                # renders.
                "global_use": True,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_incident_weekly_review``.

        IK: docs/school_incident_weekly_review/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_incident_weekly_review_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_incident_weekly_review``.

        IK: docs/school_incident_weekly_review/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_incident_weekly_review_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_incident_weekly_review``.

        IK: docs/school_incident_weekly_review/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_incident_weekly_review_approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_incident_weekly_review``.

        IK: docs/school_incident_weekly_review/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_incident_weekly_review_cancel",
            login="admin",
        )
