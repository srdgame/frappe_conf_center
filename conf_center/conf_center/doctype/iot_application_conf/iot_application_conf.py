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
