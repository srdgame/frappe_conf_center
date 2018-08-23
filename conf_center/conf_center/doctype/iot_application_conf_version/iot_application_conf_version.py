# -*- coding: utf-8 -*-
# Copyright (c) 2018, freeioe.org and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.model.document import Document


class IOTApplicationConfVersion(Document):
	def validate(self):
		self.app_conf_name = frappe.get_value("IOT Application Conf", self.conf, "conf_name")
		app = frappe.get_value("IOT Application Conf", self.conf, "app")
		self.app_name = frappe.get_value("IOT Application", app, "app_name")

		if not self.is_new():
			self.data = frappe.get_value("IOT Application Conf Version", self.name, "data")
		else:
			latest = get_latest_version(self.conf)
			if latest > self.version:
				throw(_("Version must be bigger than {0}").format(latest))


def on_doctype_update():
	"""Add indexes in `IOT Application Conf Version`"""
	frappe.db.add_index("IOT Application Conf Version", ["conf", "version"])


def get_latest_version(conf):
	sql = "select max(version) from `tabIOT Application Conf Version` where name='{0}'".format(conf)
	return frappe.db.sql(sql)[0][0]