import frappe

# This patch set the developer value from owner field


def execute():
	frappe.reload_doc('conf_center', 'doctype', 'iot_application_conf')
	table_columns = frappe.db.get_table_columns("IOT Application Conf")

	if not table_columns:
		return

	if "developer" in table_columns:
		frappe.db.sql('''
			update `tabIOT Application Conf`
			set developer = owner
			where ifnull(developer, '') = ''
		''')
		frappe.db.sql('''
			update `tabIOT Application Conf`
			set developer = owner
			where developer = '\n'
		''')

	frappe.clear_cache()