odoo.define("ssi_school_incident.school_incident_create_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/school_incident/01-create.md
    tour.register(
        "ssi_school_incident_school_incident_create",
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
                run: "text Tour Incident Student",
            },
            {
                content: "Pick the Student from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Incident Student)",
                in_modal: false,
            },
            {
                content: "Select the Incident Type",
                trigger: ".o_field_many2one[name='incident_type_id'] input",
                run: "text Academic",
            },
            {
                content: "Pick the Incident Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(Academic)",
                in_modal: false,
            },
            {
                content: "Fill in the Description",
                trigger: ".o_field_widget[name='description']",
                run: "text Tour: student was involved in a minor incident.",
            },

            // Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                // Post-Condition: the new record is created in Draft status.
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
