# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import datetime
from frappe import throw, _
from frappe.utils import convert_utc_to_user_timezone
from iot.user_api import valid_auth_code
from cloud.cloud.doctype.cloud_company.cloud_company import list_user_companies
from cloud.cloud.doctype.cloud_company_group.cloud_company_group import list_user_groups


def get_post_json_data():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))
	ctype = frappe.get_request_header("Content-Type")
	if "json" not in ctype.lower():
		throw(_("Incorrect HTTP Content-Type found {0}").format(ctype))
	data = frappe.request.get_data()
	if not data:
		throw(_("JSON Data not found!"))
	return json.loads(data.decode('utf-8'))


@frappe.whitelist(allow_guest=True)
def upload_conf_version(conf, version, data, comment=None):
	valid_auth_code()
	version_data = {
		"doctype": "IOT Application Conf Version",
		"conf": conf,
		"version": version,
		"comment": comment,
		"data": data
	}
	doc = frappe.get_doc(version_data).insert()
	return True


@frappe.whitelist(allow_guest=True)
def get_latest_version(conf):
	from conf_center.conf_center.doctype.iot_application_conf_version.iot_application_conf_version import get_latest_version
	return get_latest_version(conf)


@frappe.whitelist(allow_guest=True)
def app_conf_version(conf): ## TODO: delete this
	return get_latest_version(conf)


@frappe.whitelist(allow_guest=True)
def get_versions(conf, order_by="version desc"):
	conf_version_fields = ["name", "version", "app_name", "app_conf_name", "comment", "creation", "owner"]
	return frappe.get_all("IOT Application Conf Version", filters={"conf": conf}, fields=conf_version_fields, order_by=order_by)


@frappe.whitelist(allow_guest=True)
def app_conf_data(conf, version):
	# valid_auth_code() -- guest get conf data is allowed now!
	ver = frappe.get_value("IOT Application Conf Version", filters={"conf": conf, "version": int(version)})
	if not ver:
		return {"version": -1, "data": ""}
	doc = frappe.get_doc("IOT Application Conf Version", ver)
	return {
		"data": doc.data,
		"version": doc.version
	}


@frappe.whitelist(allow_guest=True)
def create_app_conf(app, conf_name, description, type='Template', company=None, public=1):
	valid_auth_code()

	if public is True:
		public = 1

	conf_data = {
		"doctype": "IOT Application Conf",
		"app": app,
		"conf_name": conf_name,
		"description": description,
		"type": type,
		"developer": frappe.session.user,
		"company": company,
		"public": public
	}
	doc = frappe.get_doc(conf_data).insert()
	return doc.name


@frappe.whitelist(allow_guest=True)
def modify_app_conf(name, conf_name=None, description=None, public=1):
	valid_auth_code()
	doc = frappe.get_doc('IOT Application Conf', name)
	if conf_name:
		doc.set("conf_name", conf_name)
	if description:
		doc.set("description", description)
	if description:
		doc.set("description", description)
	if public:
		doc.set("public", public)
	doc.save()
	return _("Done!")


@frappe.whitelist(allow_guest=True)
def delete_app_conf(name):
	valid_auth_code()
	frappe.delete_doc("IOT Application Conf", name)
	return _("Deleted!")


app_conf_fields = ["app", "name", "conf_name", "description", "type", "company", "developer"]


def add_more_info(conf):
	version = get_latest_version(conf=conf.name)
	version_creation = frappe.get_value("IOT Application Conf Version", {"conf": conf.name, "version": version}, "creation")
	app = frappe.get_doc("IOT Application", conf.app)
	conf.update({
		"latest_version": version,
		"latest_version_creation": version_creation,
		"app_name": app.app_name,
		"app_path": app.app_path,
		"code_name": app.code_name,
	})
	return conf


@frappe.whitelist(allow_guest=True)
def list_app_conf(app, filters=None, fields=app_conf_fields, order_by="modified desc", start=0, limit=40):
	valid_auth_code()
	filters = filters or {}
	filters.update({
		"app": app,
		"developer": ["!=", 'Administrator'],
		"public": 1,
	})

	result = frappe.get_all("IOT Application Conf", fields=fields, filters=filters, order_by=order_by, start=start, limit=limit)

	return [add_more_info(d) for d in result]


@frappe.whitelist()
def list_app_conf_pri(app, filters=None, fields=app_conf_fields, order_by="modified desc", start=0, limit=40):
	filters = filters or {}
	filters.update({
		"app": app,
		"developer": frappe.session.user
	})

	result = frappe.get_all("IOT Application Conf", fields=fields, filters=filters, order_by=order_by, start=start, limit=limit)

	return [add_more_info(d) for d in result]

#
# @frappe.whitelist()
# def list_private_conf(filters=None, fields=app_conf_fields, order_by="modified desc", start=0, limit=40):
# 	filters = filters or {}
# 	filters.update({
# 		"developer": frappe.session.user
# 	})
#
# 	pri_list = frappe.get_all("IOT Application Conf", fields=fields, filters=filters, order_by=order_by, start=start, limit=limit)
#
# 	groups = [d.name for d in list_user_groups(frappe.session.user)]
# 	filters.update({
# 		"owner_id": ["in", groups]
# 	})
# 	group_list = frappe.get_all("IOT Application Conf", fields=fields, filters=filters, order_by=order_by, start=start, limit=limit)
#
# 	pri_list = [add_more_info(d) for d in pri_list]
# 	group_list = [add_more_info(d) for d in group_list]
#
# 	return {
# 		"private": pri_list,
# 		"company": group_list,
# 	}


@frappe.whitelist()
def list_conf_company_pri(filters=None, fields=app_conf_fields, order_by="modified desc", start=0, limit=40):
	filters = filters or {}
	companies = list_user_companies()

	filters.update({
		"company": ["in", companies]
	})

	result = frappe.get_all("IOT Application Conf", fields=fields, filters=filters, order_by=order_by, start=start, limit=limit)

	return [add_more_info(d) for d in result]


@frappe.whitelist(allow_guest=True)
def app_conf_detail(name, fields=app_conf_fields):
	valid_auth_code()
	result = frappe.get_all("IOT Application Conf", fields=fields, filters={"name": name})
	if len(result) == 1:
		return add_more_info(result[0])
	return None


@frappe.whitelist(allow_guest=True)
def upload_device_conf(conf=None):
	valid_auth_code()
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
	return True


@frappe.whitelist(allow_guest=True)
def device_conf_data(name):
	# valid_auth_code() -- guest get conf data is allowed now!
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
def device_conf_list(sn):
	valid_auth_code()
	return frappe.get_all("IOT Device Conf", {"device": sn}, ["name", "timestamp", "data", "hashing"])


@frappe.whitelist(allow_guest=True)
def ping():
	return _("pong from conf_center.api.ping")
