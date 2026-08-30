odoo.define("ssi_school_incident.school_academic_alert_cancel_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/school_academic_alert/10-cancel.md
    tour.register(
        "ssi_school_incident_school_academic_alert_cancel",
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

            // Flow 2 — Open the School Academic Alert record to cancel.
            {
                content: "Open the record to cancel",
                trigger:
                    ".o_data_row:contains(Student For Alert Cancel Tour) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 3 — Click the Cancel button.
            //
            // The Cancel button is a `type="action"` button, so its
            // `name` attribute is a numeric action id in the DOM;
            // target it by label instead (patterns-dialogs-and-wizards.md
            // §H / selectors.md §4).
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — In the wizard that appears, select the
            // Cancellation Reason.
            //
            // The wizard renders cancel_reason_id with widget="radio" --
            // select the matching radio item by its label text. 14.0: do
            // NOT prefix the trigger with `.modal` (patterns-dialogs-
            // and-wizards.md §H).
            {
                content: "Select the Cancellation Reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(Tour Academic Alert Cancel Reason) input",
                in_modal: true,
            },

            // Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // Flow 6 — Click OK on the confirmation dialog.
            //
            // The wizard's own Confirm button carries
            // confirm="Are you sure?", stacking a second modal on top of
            // the wizard; 14.0 scopes the trigger search to the topmost
            // visible modal.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                // Post-Condition: status changes to Cancelled.
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
