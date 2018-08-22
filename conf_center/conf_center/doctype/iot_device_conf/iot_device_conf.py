# -*- coding: utf-8 -*-
# Copyright (c) 2018, freeioe.org and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, msgprint, _
from frappe.model.document import Document


class IOTDeviceConf(Document):
	def validate(self):
		if not self.is_new():
			self.data = frappe.get_value("IOT Device Conf", self.name, "data")
		else:
			dev = frappe.get_doc("IOT Device", self.device)
			if not dev:
				throw(_("Device not found!"))
			self.owner_company = dev.company
			self.owner_type = dev.owner_type
			self.owner_id = dev.owner_id


def on_doctype_update():
	"""Add indexes in `IOT Device Conf`"""
	frappe.db.add_index("IOT Device Conf", ["device", "owner_company"])
	frappe.db.add_index("IOT Device Conf", ["owner_type", "owner_id"])
