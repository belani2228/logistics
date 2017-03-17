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
		data.append([ri.name, ri.customer, ri.shipping_instruction, ri.no_do,
		ri.container_no, ri.no_seal, ri.lisence_plate, ri.weight, ri.vendor_trucking,
		ri.received_do, ri.date, ri.tebus_bon_muat, ri.pic_tebus_bon, ri.pick_up_start,
		ri.pick_up_done, ri.pic_pick_up, ri.cetak_kartu_kuning, ri.pic_cetak_kartu,
		ri.gate_in, ri.pic_gate_in, ri.status_container
	])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("No Job")+":Link/Rekap Export:150",
		_("Customer")+":Link/Customer:150",
		_("Shipping Instruction")+"::100",
		_("DO")+"::100",
		_("No Container")+"::100",
		_("No Seal")+"::100",
		_("No Mobil")+"::100",
		_("Weight")+":Float:100",
		_("Trucking")+"::100",
		_("Tgl Terima DO")+":Datetime:120",
		_("Tgl Stuffing")+":Datetime:120",
		_("Tebus Bon Muat")+"::100",
		_("PIC")+":Link/Employee:120",
		_("Tgl Pick Up Start")+":Datetime:120",
		_("Tgl Pick Up Done")+":Datetime:120",
		_("PIC")+":Link/Employee:120",
		_("Tgl Cetak Kartu Kuning")+":Datetime:120",
		_("PIC")+":Link/Employee:120",
		_("Tgl Gate In Pelabuhan")+":Datetime:120",
		_("PIC")+":Link/Employee:120",
		_("Status Container")+"::100",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("no_job"):
		conditions += " and p1.`name` = '%s'" % frappe.db.escape(filters["no_job"])

	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""SELECT p1.name, p1.customer, p1.shipping_instruction,
	p1.no_do, p2.container_no, p2.no_seal, p2.license_plate, p2.weight,
	p2.vendor_trucking, p1.received_do, p2.date, p2.tebus_bon_muat, p2.pic_tebus_bon,
	p2.pick_up_start, p2.pick_up_done, p2.pic_pick_up, p2.cetak_kartu_kuning,
	p2.pic_cetak_kartu, p2.gate_in, p2.pic_gate_in, p2.status_container
	FROM `tabRekap Export` p1
	INNER JOIN `tabRekap Export Item` p2 ON p1.name = p2.parent
	WHERE p1.docstatus != '2' %s
	ORDER BY p1.`name` DESC""" %
		conditions, as_dict=1)
