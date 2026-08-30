odoo.define("ssi_school_incident.school_academic_alert_level_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/school_academic_alert_level/01-create.md
    tour.register(
        "ssi_school_incident_school_academic_alert_level_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the School > Configuration > Incident >
            // Academic Alert Levels menu. "Incident" (level 3) has
            // children so it renders as a non-clickable dropdown header
            // without a data-menu-xmlid — skip straight to the leaf.
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
                content: "Open the Academic Alert Levels menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_incident.school_academic_alert_level_menu"]',
            },
            {
                // Gerbang: tunggu action tujuan benar-benar terpasang.
                content: "Academic Alert Levels list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Academic Alert Levels)",
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
                run: "text Yellow - Early Warning",
            },
            {
                content: "Open the Trigger tab",
                trigger: ".o_notebook .nav-link:contains(Trigger)",
            },
            {
                content: "Select the Color",
                trigger: "select.o_field_widget[name='color']",
                run: "text Yellow",
            },
            {
                content: "Fill in Sequence",
                trigger: ".o_field_widget[name='sequence']",
                run: "text 10",
            },
            {
                content: "Fill in Python Code",
                trigger: ".o_field_widget[name='python_code']",
                run: "text result = trigger_count >= 2",
            },
            {
                content: "Open the Action & SLA tab",
                trigger: ".o_notebook .nav-link:contains(Action & SLA)",
            },
            {
                content: "Fill in Action Guideline",
                trigger: ".o_field_widget[name='action_guideline']",
                run: "text Notify homeroom teacher and parent.",
            },
            {
                content: "Fill in SLA",
                trigger: ".o_field_widget[name='sla_text']",
                run: "text Contact parent within 24 hours.",
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
