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
		data.append([
			ri.item_code, ri.selling_import, ri.selling_export, ri.selling_total
		])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Item Code")+":Link/Item:200",
		_("Import")+":Currency:150",
		_("Export")+":Currency:150",
		_("Total")+":Currency:150",
	]

	return columns

def get_entries(filters):
	cust = filters.get("customer")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	return frappe.db.sql("""select distinct(jci.item_code),
			(select	sum(a1.selling) from `tabJob Cost Item` a1	inner join `tabJob Cost` a2 on a1.parent = a2.`name`
			where a2.jenis_rekap = 'Rekap Import' and a1.item_code = jci.item_code and a2.customer = '%(cust)s' and a2.date >= '%(from)s' and a2.date <= '%(to)s')
			as selling_import,
			(select	sum(b1.selling) from `tabJob Cost Item` b1	inner join `tabJob Cost` b2 on b1.parent = b2.`name`
			where b2.jenis_rekap = 'Rekap Export' and b1.item_code = jci.item_code and b2.customer = '%(cust)s' and b2.date >= '%(from)s' and b2.date <= '%(to)s')
			as selling_export,
			(select	sum(c1.selling) from `tabJob Cost Item` c1	inner join `tabJob Cost` c2 on c1.parent = c2.`name`
			where c1.item_code = jci.item_code and c2.customer = '%(cust)s' and c2.date >= '%(from)s' and c2.date <= '%(to)s')
			as selling_total
		from `tabJob Cost` jc
		inner join `tabJob Cost Item` jci on jc.`name` = jci.parent
		where jc.docstatus != '2' and jc.customer = '%(cust)s' and jc.date >= '%(from)s' and jc.date <= '%(to)s'
		order by item_code asc""" %
		{"from": from_date, "to": to_date, "cust": cust}, as_dict=1)
