# -*- coding: utf-8 -*-
# Copyright (c) 2018, freeioe.org and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class IOTApplicationConfVersion(Document):
	def validate(self):
		self.app_conf_name = frappe.get_value("IOT Application Conf", self.conf, "conf_name")
		app = frappe.get_value("IOT Application Conf", self.conf, "app")
		self.app_name = frappe.get_value("IOT Application", app, "app_name")

		if not self.is_new():
			self.data = frappe.get_value("IOT Application Conf Version", self.name, "data")
