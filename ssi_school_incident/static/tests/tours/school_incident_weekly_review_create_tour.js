odoo.define("ssi_school_incident.school_incident_weekly_review_create_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/school_incident_weekly_review/01-create.md
    tour.register(
        "ssi_school_incident_school_incident_weekly_review_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the School > Incident > Weekly Case
            // Reviews menu.
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
                content: "Open the Weekly Case Reviews menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_incident.school_incident_weekly_review_menu"]',
            },
            {
                // Gerbang: tunggu action tujuan benar-benar terpasang.
                content: "Weekly Case Reviews list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Weekly Case Reviews)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 2 — Click the New button.
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 3/4 — Date Start and Date End are already
            // populated by their defaults (7 days ago / today) and
            // School is optional, so no field needs to be touched
            // before saving.

            // Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                // Post-Condition: the new record is created in
                // Draft status.
                content: "Record is saved in Draft",
                trigger:
                    ".o_form_view.o_form_readonly .o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
