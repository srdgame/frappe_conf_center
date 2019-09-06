# -*- coding: utf-8 -*-
# Copyright (c) 2018, freeioe.org and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw,_
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
		if not self.owner_id:
			if self.owner_type == "Cloud Company Group":
				from cloud.cloud.doctype.cloud_company.cloud_company import list_user_companies
				companies = list_user_companies(frappe.session.user)
				self.owner_id = frappe.get_value("Cloud Company Group", {"company": companies[0], "group_name": "root"})
			else:
				self.owner_id = frappe.session.user
		if not self.owner_id:
			throw(_("You have not specify the owner, as we cannot detected it!"))

		self.unique_name = self.app + '/' + self.owner_id + "/" + self.conf_name
		if self.owner_type == "Cloud Company Group":
			self.owner_company = frappe.get_value("Cloud Company Group", self.owner_id, "company")
		else:
			self.owner_company = None

	def clean_before_delete(self):
		if not self.has_permission("write"):
			raise frappe.PermissionError

		for d in frappe.db.get_values("IOT Application Conf Version", {"conf": self.name}, "name"):
			frappe.delete_doc("IOT Application Conf Version", d[0])

	def append_keywords(self, *keywords):
		"""Add groups to user"""
		current_keywords = [d.key for d in self.get("keywords")]
		for key in keywords:
			if key in current_keywords:
				continue
			self.append("keywords", {"key": key})

	def add_keywords(self, *keywords):
		"""Add groups to user and save"""
		self.append_keywords(*keywords)
		self.save()

	def remove_keywords(self, *keywords):
		existing_keywords = dict((d.key, d) for d in self.get("keywords"))
		for key in keywords:
			if key in existing_keywords:
				self.get("keywords").remove(existing_keywords[key])
		self.save()


def on_doctype_update():
	"""Add indexes in `IOT Application Conf`"""
	frappe.db.add_index("IOT Application Conf", ["app", "owner_type", "owner_id"])
	frappe.db.add_index("IOT Application Conf", ["owner_company"])


def list_tags(conf):
	return []


def add_tags(conf, *tags):
	return tags


def remove_tags(conf, *tags):
	return []


def clear_tags(conf):
	return []
