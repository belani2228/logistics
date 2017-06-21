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
		data.append([pl.customer, pl.export_cost, pl.export_sell, pl.export_profit,
		pl.import_cost, pl.import_sell, pl.import_profit, pl.total_profit])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Customer")+":Link/Customer:140",
		_("Export Cost")+":Currency:110",
		_("Export Selling")+":Currency:110",
		_("Profit Export")+":Currency:110",
		_("Import Cost")+":Currency:110",
		_("Import Selling")+":Currency:110",
		_("Profit Import")+":Currency:110",
		_("Total Profit")+":Currency:110",
	]

	return columns

#def get_conditions(filters):
#	conditions = ""
#	if filters.get("from_date"):
#		conditions += " and date >= '%s'" % frappe.db.escape(filters["from_date"])
#	if filters.get("to_date"):
#		conditions += " and date <= '%s'" % frappe.db.escape(filters["to_date"])

#	return conditions

def get_entries(filters):
#	conditions = get_conditions(filters)
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	return frappe.db.sql("""select distinct(a.customer),
	(select sum(ec.total_cost) from `tabJob Cost` ec where ec.customer = a.customer and ec.jenis_rekap = 'Rekap Export' and ec.date >= '%(from)s' and ec.date <= '%(to)s') as export_cost,
	(select sum(es.total_selling) from `tabJob Cost` es where es.customer = a.customer and es.jenis_rekap = 'Rekap Export' and es.date >= '%(from)s' and es.date <= '%(to)s') as export_sell,
	(select sum(p1.profit_loss) from `tabJob Cost` p1 where p1.customer = a.customer and p1.jenis_rekap = 'Rekap Export' and p1.date >= '%(from)s' and p1.date <= '%(to)s') as export_profit,
	(select sum(ic.total_cost) from `tabJob Cost` ic where ic.customer = a.customer and ic.jenis_rekap = 'Rekap Import' and ic.date >= '%(from)s' and ic.date <= '%(to)s') as import_cost,
	(select sum(ij.total_selling) from `tabJob Cost` ij where ij.customer = a.customer and ij.jenis_rekap = 'Rekap Import' and ij.date >= '%(from)s' and ij.date <= '%(to)s') as import_sell,
	(select sum(p2.profit_loss) from `tabJob Cost` p2 where p2.customer = a.customer and p2.jenis_rekap = 'Rekap Import' and p2.date >= '%(from)s' and p2.date <= '%(to)s') as import_profit,
	(select sum(tp.profit_loss) from `tabJob Cost` tp where tp.customer = a.customer and tp.date >= '%(from)s' and tp.date <= '%(to)s') as total_profit
	from `tabJob Cost` a
	where a.docstatus != '2' and a.date >= '%(from)s' and a.date <= '%(to)s'
	order by a.customer asc""" %
		{"from": from_date, "to": to_date}, as_dict=1)
