odoo.define("ssi_school_incident.school_academic_alert_create_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/school_academic_alert/01-create.md
    tour.register(
        "ssi_school_incident_school_academic_alert_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the School > Incident > Academic Alerts menu.
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
                content: "Open the Academic Alerts menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_incident.school_academic_alert_menu"]',
            },
            {
                // Gerbang: tunggu action tujuan benar-benar terpasang.
                content: "Academic Alerts list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Academic Alerts)",
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

            // Flow 3 — Fill in the required fields.
            {
                content: "Select the Student",
                trigger: ".o_field_many2one[name='student_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Academic Alert Student",
            },
            {
                content: "Pick the Student from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Academic Alert Student)",
                in_modal: false,
            },

            // Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                // Post-Condition: the new record is created in Draft
                // status, with no Alert Level set yet.
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
