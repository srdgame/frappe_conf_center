# -*- coding: utf-8 -*-
# Copyright (c) 2018, freeioe.org and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


 # searches for active employees
def iot_application_query(doctype, txt, searchfield, start, page_len, filters):
	if 'System Manager' in frappe.get_roles(frappe.session.user):
		return frappe.db.sql("""select name, app_name, owner, category from `tabIOT Application`
			order by
				if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
				if(locate(%(_txt)s, app_name), locate(%(_txt)s, app_name), 99999),
				idx desc,
				name, app_name
			limit %(start)s, %(page_len)s""", {
				'txt': "%%%s%%" % txt,
				'_txt': txt.replace("%", ""),
				'start': start,
				'page_len': page_len
			})

	return frappe.db.sql("""select name, app_name, owner, category from `tabIOT Application`
		where owner != 'Administrator' 
			and ({key} like %(txt)s
				or app_name like %(txt)s)
			and (owner = '{user}'
				or published = 1)
			and license_type = 'Open'
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, app_name), locate(%(_txt)s, app_name), 99999),
			idx desc,
			name, app_name
		limit %(start)s, %(page_len)s""".format(**{
			'key': searchfield,
			'user': frappe.session.user
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})