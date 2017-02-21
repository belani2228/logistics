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

	for cl in sl_entries:
		data.append([cl.parent, cl.no_do, cl.carrier, cl.vessel, cl.qty, cl.size,
		cl.type, cl.pod, cl.container_no, cl.gate_in, cl.open_cy, cl.clossing_cy,
		cl.gate_out, cl.within_days])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("No Job")+":Link/Task:140",
		_("DO")+"::100",
		_("Carrier")+":Link/Supplier:140",
		_("Vessel")+"::140",
		_("QTY")+":Float:60",
		_("Size")+":50",
		_("Type")+"::50",
		_("Destination")+"::150",
		_("No Container")+"::130",
		_("Gate In")+":Datetime:150",
		_("Open CY")+":Datetime:150",
		_("Clossing CY")+":Datetime:150",
		_("Gate Out")+":Datetime:150",
		_("Waktu Penitipan")+":Float:120",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("no_rekap"):
		conditions += " and cl.parent = '%s'" % frappe.db.escape(filters["no_rekap"])

	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""SELECT cl.parent, re.no_do, re.carrier, re.vessel,
	re.qty, re.size, re.type, re.pod, cl.container_no, cl.gate_in, re.open_cy,
	re.clossing_cy, cl.gate_out, cl.within_days
	FROM `tabContainer List` cl
	INNER JOIN `tabRekap Export` re ON cl.parent = re.name
	WHERE cl.docstatus != '2' %s
	ORDER BY cl.parent ASC""" %
		conditions, as_dict=1)
