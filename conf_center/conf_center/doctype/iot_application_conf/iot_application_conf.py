# -*- coding: utf-8 -*-
# Copyright (c) 2018, freeioe.org and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class IOTApplicationConf(Document):
	def autoname(self):
		if self.type == "Template":
			self.name = make_autoname('TPL.#########')
		elif self.type == "Configuration":
			self.name = make_autoname('CNF.#########')
		else:
			self.name = make_autoname('IAF.#########')

	def validate(self):
		self.unique_name = self.owner_id + "/" + self.conf_name
		if self.owner_type == "Cloud Company Group":
			self.owner_company = frappe.get_value("Cloud Company Group", self.owner_id, "company")
		else:
			self.owner_company = None


def on_doctype_update():
	"""Add indexes in `IOT Application Conf`"""
	frappe.db.add_index("IOT Application Conf", ["app", "owner_type", "owner_id"])
	frappe.db.add_index("IOT Application Conf", ["owner_company"])