# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Configuration Center"),
			"items": [
				{
					"type": "doctype",
					"name": "IOT Application Conf",
					"onboard": 1,
					"description": _("IOT Application Conf"),
				},
				{
					"type": "doctype",
					"name": "IOT Application Conf Version",
					"onboard": 1,
					"description": _("IOT Application Conf Version"),
				},
				{
					"type": "doctype",
					"name": "IOT Device Conf",
					"onboard": 1,
					"description": _("IOT Device Conf"),
				}
			]
		}
	]
