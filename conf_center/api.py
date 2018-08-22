# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import datetime
from frappe import throw, msgprint, _
from frappe.utils import now, get_datetime, convert_utc_to_user_timezone
from iot.user_api import valid_auth_code


def get_post_json_data():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))
	ctype = frappe.get_request_header("Content-Type")
	if "json" not in ctype.lower():
		throw(_("Incorrect HTTP Content-Type found {0}").format(ctype))
	data = frappe.request.get_data()
	if not data:
		throw(_("JSON Data not found!"))
	return json.loads(data)


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
	ver = frappe.get_value("IOT Application Conf Version", filters={"conf": conf, "version": int(version)})
	if not ver:
		return {"version": -1, "data": ""}
	doc = frappe.get_doc("IOT Application Conf Version", ver)
	return {
		"data": doc.data,
		"version": doc.version
	}



@frappe.whitelist(allow_guest=True)
def upload_device_conf(conf=None):
	# valid_auth_code()
	conf = conf or get_post_json_data()

	ts = datetime.datetime.utcfromtimestamp(int(conf.get("timestamp")))
	ts = convert_utc_to_user_timezone(ts).replace(tzinfo=None)
	dev_conf = {
		"doctype": "IOT Device Conf",
		"device": conf.get("sn"),
		"timestamp": ts,
		"data": conf.get("data"),
		"hashing": conf.get("md5")
	}
	doc = frappe.get_doc(dev_conf).insert(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def device_conf_data(name):
	doc = frappe.get_doc("IOT Device Conf", name)
	if not doc:
		throw(_("Device Conf Data not exits!"))

	return {
		"device": doc.device,
		"timestamp": doc.timestamp,
		"data": doc.data,
		"md5": doc.hashing
	}


@frappe.whitelist(allow_guest=True)
def ping():
	return _("pong")