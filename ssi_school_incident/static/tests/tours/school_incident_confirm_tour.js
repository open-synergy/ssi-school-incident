odoo.define("ssi_school_incident.school_incident_confirm_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/school_incident/04-confirm.md
    tour.register(
        "ssi_school_incident_school_incident_confirm",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the School > Incident > Incidents menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Incident menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_incident.menu_incident_root"]',
            },
            {
                content: "Open the Incidents menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_incident.school_incident_menu"]',
            },
            {
                // Gerbang: tunggu action tujuan benar-benar terpasang.
                content: "Incidents list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Incidents)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 2 — Open the School Incident record to confirm.
            {
                content: "Open the record to confirm",
                trigger:
                    ".o_data_row:contains(Student For Confirm Tour) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 3 — Click the Confirm button.
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                // Post-Condition: status changes to Waiting for Approval.
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
