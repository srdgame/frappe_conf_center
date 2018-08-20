# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import os
import requests
from frappe import throw, msgprint, _
from frappe.utils import now, get_datetime, convert_utc_to_user_timezone
from werkzeug.utils import secure_filename
from iot.iot.user_api import valid_auth_code


@frappe.whitelist(allow_guest=True)
def upload_conf_version(sn, app, conf, version, data):
	valid_auth_code()
	version_data = {
		"doctype": "IOT Application Conf Version",
		"app": app,
		"conf": conf,
		"version": version,
		"data": data
	}
	doc = frappe.get_doc(version_data).insert()


@frappe.whitelist(allow_guest=True)
def app_conf_version(sn, app, conf):
	vlist = [d[0] for d in frappe.db.get_values("IOT Application Conf Version", conf, "version")]
	if not vlist:
		return None
	return max(vlist)


@frappe.whitelist(allow_guest=True)
def app_conf_data(app, conf, version):
	return frappe.db.get_values("IOT Application Conf Version", conf, {"data", "version"})


@frappe.whitelist(allow_guest=True)
def dev_conf(sn, timestamp, data, md5):
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	dev_conf = {
		"doctype": "IOT Device Conf",
		"device": sn,
		"timestamp": get_datetime(timestamp),
		"data": data,
		"hashing": md5
	}
	doc = frappe.get_doc(dev_conf).insert()



@frappe.whitelist(allow_guest=True)
def dev_conf_content(sn):
	return ""
