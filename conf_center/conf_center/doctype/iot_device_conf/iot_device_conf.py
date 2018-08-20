# -*- coding: utf-8 -*-
# Copyright (c) 2018, freeioe.org and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class IOTDeviceConf(Document):
	pass



def on_doctype_update():
	"""Add indexes in `IOT Device Event`"""
	frappe.db.add_index("IOT Device Event", ["device", "owner_company"])
	frappe.db.add_index("IOT Device Event", ["owner_type", "owner_id"])
