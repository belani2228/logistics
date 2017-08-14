# Copyright (c) 2013, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	columns = get_columns()
	sl_entries = get_entries(filters)
	data = []

	for ri in sl_entries:
		data.append([ri.name, ri.customer_name, ri.customer_group, ri.territory,
		ri.status, ri.npwp, ri.domisili, ri.siup_tdp])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Customer")+":Link/Customer:250",
		_("Customer Name")+"::250",
		_("Customer Group")+"::120",
		_("Territory")+"::110",
		_("Status")+"::85",
		_("NPWP")+"::70",
		_("Doisili")+"::70",
		_("SIUP & TDP")+"::75",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("customer"):
		conditions += " and customer = '%s'" % frappe.db.escape(filters["customer"])
	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""SELECT `name`, customer_name, customer_group, territory,
	if(disabled = '0', "Aktif", "Tidak Aktif") as `status`,
	if(npwp = '1', '&#10004', '-') as npwp,
	if(domisili = '1', '&#10004', '-') as domisili,
	if(siup_tdp = '1', '&#10004', '-') as siup_tdp
	FROM `tabCustomer`
	WHERE docstatus != '2' %s
	ORDER BY modified DESC""" %
		conditions, as_dict=1)
