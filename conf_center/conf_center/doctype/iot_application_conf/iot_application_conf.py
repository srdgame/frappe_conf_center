# -*- coding: utf-8 -*-
# Copyright (c) 2018, freeioe.org and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw,_
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from cloud.cloud.doctype.cloud_company.cloud_company import list_user_companies


class IOTApplicationConf(Document):
	def autoname(self):
		if self.type == "Template":
			self.name = make_autoname('TPL.#########')
		elif self.type == "Configuration":
			self.name = make_autoname('CNF.#########')
		else:
			self.name = make_autoname('IAF.#########')

	def validate(self):
		if not self.developer and self.is_new():
			self.developer = frappe.session.user

		if self.company is not None:
			if self.company not in list_user_companies(self.developer):
				throw(_("You are not in company {0}".format(self.company)))

		dev_comp = self.developer if self.company is None else self.company
		self.unique_name = self.app + '/' + dev_comp + "/" + self.conf_name

	def clean_before_delete(self):
		if not self.has_permission("write"):
			raise frappe.PermissionError

		for d in frappe.db.get_values("IOT Application Conf Version", {"conf": self.name}, "name"):
			frappe.delete_doc("IOT Application Conf Version", d[0])


def on_doctype_update():
	"""Add indexes in `IOT Application Conf`"""
	frappe.db.add_index("IOT Application Conf", ["app", "company", "developer"])
