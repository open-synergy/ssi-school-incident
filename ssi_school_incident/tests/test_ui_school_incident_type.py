# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. See structure-and-runner.md "Base class".
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolIncidentType(HttpSavepointCase):
    """Tour tests for the ``school_incident_type`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group the master data menu requires."""
        super().setUpClass()
        # Pre-Condition: this master data menu is gated by
        # school_incident_type_group. Without it the tour dies on its
        # FIRST step -- the menu is never rendered.
        group = cls.env.ref("ssi_school_incident.school_incident_type_group")
        group.sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})

    def test_create(self):
        """Run the create tour for ``school_incident_type``.

        IK: docs/school_incident_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_incident_school_incident_type_create",
            login="admin",
        )
