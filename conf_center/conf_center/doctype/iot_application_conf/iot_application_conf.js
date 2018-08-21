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

	}
});
