// Copyright (c) 2018, freeioe.org and contributors
// For license information, please see license.txt

frappe.ui.form.on('IOT Application Conf', {
	setup: function(frm) {
		frm.fields_dict['app'].get_query  = function(){
			return {
				query:"conf_center.controllers.queries.iot_application_query"
			};
		};
	},
	refresh: function(frm) {
		if (frappe.user.has_role(['Administrator','App Manager'])) {
			frm.add_custom_button(__("Clean Before Delete This"), function () {
				frm.events.clean_before_delete(frm);
			}).removeClass("btn-default").addClass("btn-warning");
		}
	},
	clean_before_delete: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "clean_before_delete",
			freeze: true,
			callback: function(r) {
				if(!r.exc) frm.refresh_fields();
			}
		})
	}
});
