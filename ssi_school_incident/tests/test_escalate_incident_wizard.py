# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEscalateIncidentWizard(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Scenario tests for the ``escalate_incident`` wizard.

    Covers ``action_escalate_wizard``: the happy path where an Open
    incident is escalated through the wizard, and the negative path
    where the wizard's own ``escalate_ok`` policy check rejects a
    Draft incident instead of silently transitioning it. The
    underlying ``school_incident.action_escalate`` guards (empty
    criteria, mismatched criteria) are covered separately in
    ``test_data_school_incident.yaml``.
    """

    def test_escalate_incident_wizard(self):
        """Run every ``escalate_incident`` wizard scenario from YAML."""
        self.run_yaml_scenario("test_data_escalate_incident_wizard.yaml")
