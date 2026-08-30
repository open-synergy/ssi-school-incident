# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolIncidentWeeklyReview(YamlTransactionCase):
    """Scenario tests for ``school_incident_weekly_review``.

    Covers the simplified Draft -> Confirm -> Done approval workflow,
    cancellation and restart, the scoping applied by
    ``action_collect_incidents`` (date range, and School when set), the
    overdue / escalated / unresolved-over-7-days counters computed from
    the collected incidents, and the ``ir.actions.act_window`` dict
    returned by the four ``action_view_*`` stat buttons.
    """

    def test_school_incident_weekly_review(self):
        """Run every ``school_incident_weekly_review`` scenario from YAML.

        Includes the workflow, collect-scoping and counter scenarios
        declared in ``test_data_school_incident_weekly_review.yaml``.
        """
        self.run_yaml_scenario("test_data_school_incident_weekly_review.yaml")

    def _create_stat_action_fixtures(self):
        """Build one review with incidents split across every subset.

        Reused by the four ``action_view_*`` tests below, so each one
        only has to build the action call and its assertions. The
        recipe matches the one already proven in ``test_data_school_
        incident_weekly_review.yaml`` ("Counters For Overdue Escalated
        And Unresolved Over Seven Days"): a resolved-on-time incident
        (neither overdue nor unresolved), an unresolved incident more
        than 7 days old (overdue AND unresolved-over-7d), and an
        escalated incident more than 7 days old (overdue, but excluded
        from unresolved-over-7d because it is already escalated).

        :return: ``(review, resolved, unresolved, escalated)`` tuple of
            the created ``school_incident_weekly_review`` and its three
            collected ``school_incident`` records
        """
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type for Weekly Review Stat Action Test",
                "code": "GTWRSTAT",
                "sequence": 10,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School for Weekly Review Stat Action Test",
                "code": "SCHWRSTAT",
                "grade_type_id": grade_type.id,
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Weekly Review Stat Action Student Contact"}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student for Weekly Review Stat Action Test",
                "code": "STUWRSTAT",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        incident_type = self.env["school_incident_type"].create(
            {
                "name": "Incident Type Weekly Review Stat Action",
                "code": "INCTYPE-WR-STAT",
            }
        )

        now = datetime.now()
        resolved = self.env["school_incident"].create(
            {
                "date_incident": (now - timedelta(days=10)).date(),
                "date_first_contact": now - timedelta(days=10),
                "date_resolved": (now - timedelta(days=9)).date(),
                "student_id": student.id,
                "incident_type_id": incident_type.id,
                "handling_level": "1",
                "description": "Stat action test - resolved on time.",
                "resolution_status": "resolved_satisfied",
            }
        )
        unresolved = self.env["school_incident"].create(
            {
                "date_incident": (now - timedelta(days=10)).date(),
                "student_id": student.id,
                "incident_type_id": incident_type.id,
                "handling_level": "1",
                "description": "Stat action test - unresolved and overdue.",
                "resolution_status": "not_resolved",
            }
        )
        escalated = self.env["school_incident"].create(
            {
                "date_incident": (now - timedelta(days=10)).date(),
                "student_id": student.id,
                "incident_type_id": incident_type.id,
                "handling_level": "3",
                "description": "Stat action test - escalated and overdue.",
                "resolution_status": "escalated",
            }
        )

        review = self.env["school_incident_weekly_review"].create(
            {
                "school_id": school.id,
                "date_start": (now - timedelta(days=15)).date(),
                "date_end": now.date(),
            }
        )
        review.write(
            {"incident_ids": [(6, 0, (resolved + unresolved + escalated).ids)]}
        )
        review.invalidate_cache()
        return review, resolved, unresolved, escalated

    def test_action_view_total_incidents(self):
        """Assert the action returned by ``action_view_total_incidents``.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value, so YAML cannot assert the ``ir.actions.act_
        window`` dict this method returns at all). Asserts ``res_
        model`` and that ``domain`` selects exactly every collected
        incident -- not more, not fewer.
        """
        review, resolved, unresolved, escalated = self._create_stat_action_fixtures()
        action = review.action_view_total_incidents()
        expected_ids = set((resolved + unresolved + escalated).ids)

        self.assertEqual(action["res_model"], "school_incident")
        self.assertEqual(action["domain"][0][:2], ("id", "in"))
        self.assertEqual(set(action["domain"][0][2]), expected_ids)

    def test_action_view_overdue_incidents(self):
        """Assert the action from ``action_view_overdue_incidents``.

        Pure Python -- trigger P1 (L-01), same rationale as ``test_
        action_view_total_incidents``. Asserts ``domain`` selects
        exactly the two overdue incidents (unresolved and escalated)
        and excludes the one resolved on time.
        """
        review, resolved, unresolved, escalated = self._create_stat_action_fixtures()
        action = review.action_view_overdue_incidents()
        expected_ids = set((unresolved + escalated).ids)
        actual_ids = set(action["domain"][0][2])

        self.assertEqual(action["res_model"], "school_incident")
        self.assertEqual(actual_ids, expected_ids)
        self.assertNotIn(resolved.id, actual_ids)

    def test_action_view_unresolved_over_7d_incidents(self):
        """Assert the action from ``action_view_unresolved_over_7d_
        incidents``.

        Pure Python -- trigger P1 (L-01), same rationale as ``test_
        action_view_total_incidents``. Asserts ``domain`` selects only
        the unresolved incident and excludes both the resolved-on-time
        one and the escalated one (an escalated case is deliberately
        excluded from this counter -- see ``UNRESOLVED_RESOLUTION_
        STATUSES`` in the model).
        """
        review, resolved, unresolved, escalated = self._create_stat_action_fixtures()
        action = review.action_view_unresolved_over_7d_incidents()
        expected_ids = {unresolved.id}
        actual_ids = set(action["domain"][0][2])

        self.assertEqual(action["res_model"], "school_incident")
        self.assertEqual(actual_ids, expected_ids)
        self.assertNotIn(escalated.id, actual_ids)
        self.assertNotIn(resolved.id, actual_ids)

    def test_action_view_escalated_incidents(self):
        """Assert the action from ``action_view_escalated_incidents``.

        Pure Python -- trigger P1 (L-01), same rationale as ``test_
        action_view_total_incidents``. Asserts ``domain`` selects only
        the escalated incident.
        """
        review, resolved, unresolved, escalated = self._create_stat_action_fixtures()
        action = review.action_view_escalated_incidents()
        expected_ids = {escalated.id}
        actual_ids = set(action["domain"][0][2])

        self.assertEqual(action["res_model"], "school_incident")
        self.assertEqual(actual_ids, expected_ids)
        self.assertNotIn(unresolved.id, actual_ids)
        self.assertNotIn(resolved.id, actual_ids)
