odoo.define("ssi_school_incident.school_incident_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/school_incident_type/01-create.md
    tour.register(
        "ssi_school_incident_school_incident_type_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the School > Configuration > Incident >
            // Incident Types menu. "Incident" (level 3) has children so
            // it renders as a non-clickable dropdown header without a
            // data-menu-xmlid — skip straight to the leaf.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
            },
            {
                content: "Open the Incident Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_incident.school_incident_type_menu"]',
            },
            {
                // Gerbang: tunggu action tujuan benar-benar terpasang.
                content: "Incident Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Incident Types)",
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
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },
            {
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Bullying",
            },
            {
                content: "Open the Handling tab",
                trigger: ".o_notebook .nav-link:contains(Handling)",
            },
            {
                content: "Select the Default Handling Level",
                trigger: "select.o_field_widget[name='default_handling_level']",
                run: "text Tier 1 - Homeroom Teacher",
            },
            {
                content: "Fill in First Contact SLA (Hour)",
                trigger: ".o_field_widget[name='first_contact_sla_hour']",
                run: "text 24",
            },

            // Flow 4 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                // Post-Condition: the new record is created and active.
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
