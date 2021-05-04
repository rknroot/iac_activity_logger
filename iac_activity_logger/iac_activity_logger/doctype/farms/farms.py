# -*- coding: utf-8 -*-
# Copyright (c) 2021, Eco Data & IAC and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class Farms(Document):
	pass

@frappe.whitelist()
def get_permissions(user):
	retval = ''
	if "System Manager" in frappe.permissions.get_roles(frappe.session.user):
		pass
	elif "Farm Admin" in frappe.permissions.get_roles(frappe.session.user):
		retval = """((`tabFarms`.admin = '{user}'))""".format(user=frappe.session.user)

	elif "Farm Supervisor" in frappe.permissions.get_roles(frappe.session.user):
		retval = """((`tabFarms`.supervisor = '{user}'))""".format(user=frappe.session.user)
	return retval
