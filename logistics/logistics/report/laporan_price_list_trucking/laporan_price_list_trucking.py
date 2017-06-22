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

	for pl in sl_entries:
		data.append([pl.vendor, pl.customer, pl.wilayah, pl.size, pl.type, pl.buying, pl.selling])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Vendor")+":Link/Supplier:140",
		_("Customer")+":Link/Customer:140",
		_("Wilayah")+":Link/Region:120",
		_("Size")+"::80",
		_("Type")+"::50",
		_("Harga Beli")+":Currency:110",
		_("Harga Jual")+":Currency:110",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("vendor"):
		conditions += " and tp.vendor = '%s'" % frappe.db.escape(filters["vendor"])
	if filters.get("region"):
		conditions += " and tp.wilayah = '%s'" % frappe.db.escape(filters["region"])
	if filters.get("customer"):
		conditions += " and tp.customer = '%s'" % frappe.db.escape(filters["customer"])

	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select tp.vendor, tpi.size_cont, tpi.type, tpi.selling, tpi.buying, tp.customer, tp.wilayah,
	if(tpi.type = 'CBM', CONCAT(cast(tpi.`from` as decimal(0)), " - ", cast(tpi.`to` as decimal(0))), if(tpi.type = 'KGS', CONCAT(cast(tpi.`from` as decimal(0)), " - ", cast(tpi.`to` as decimal(0))), tpi.size_cont)) AS size
	from `tabTrucking Price List` tp
	inner join `tabTrucking Price List Item` tpi on tp.`name` = tpi.parent
	where tp.docstatus = '1' %s""" %
		conditions, as_dict=1)
