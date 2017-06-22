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
		data.append([ri.no_job,
			ri.shipping_insturction,
			ri.do, ri.carrier, ri.vessel, ri.party, ri.pod,
			ri.container_no, ri.gate_in_date, ri.gate_in_time,
			ri.open_cy, ri.clossing_cy, ri.gate_out_date, ri.gate_out_time,
			ri.waktu_penitipan, ri.storage, ri.total_storage, ri.lolo,
			ri.admin, ri.total_penitipan])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("No Job")+":Link/Rekap Export:150",
		_("Shipping Instruction")+"::100",
		_("DO")+"::100",
		_("Carrier")+":Link/Supplier:100",
		_("Vessel")+"::100",
		_("Destination")+":Link/Port:100",
		_("No Container")+"::100",
		_("Party")+"::100",
		_("Gate In (Date)")+":Date:90",
		_("Gate In (Time)")+":Time:90",
		_("Open CY")+":Datetime:100",
		_("Clossing CY")+":Datetime:100",
		_("Gate Out (Date)")+":Date:90",
		_("Gate Out (Time)")+":Time:90",
		_("Waktu Penitipan")+":Float:100",
		_("Storage")+":Currency:100",
		_("Total Storage")+":Currency:100",
		_("LOLO")+":Currency:100",
		_("Admin")+":Currency:100",
		_("Total Penitipan")+":Currency:100",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("no_job"):
		conditions += " and p1.no_job = '%s'" % frappe.db.escape(filters["no_job"])

	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""SELECT p1.no_job, p1.shipping_instruction, p1.do, p1.carrier,
	p1.vessel, p1.party, p1.pod, p2.container_no, p2.gate_in_date, p2.gate_in_time,
	p1.open_cy, p1.clossing_cy, p2.gate_out_date, p2.gate_out_time,
	p2.waktu_penitipan, p2.storage, p2.total_storage, p2.lolo, p2.admin,
	p2.total_penitipan
	FROM `tabPenitipan Container` p1
	INNER JOIN `tabPenitipan Container Item` p2 ON p1.name = p2.parent
	WHERE p1.docstatus != '2' %s
	ORDER BY p1.`name` ASC""" %
		conditions, as_dict=1)
