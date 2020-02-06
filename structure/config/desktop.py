# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Structure",
			"color": "grey",
			"icon": "octicon octicon-gear",
			"type": "module",
			"label": _("Setup")
		}
	]
