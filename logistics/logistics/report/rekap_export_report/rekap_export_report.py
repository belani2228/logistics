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
		data.append([ri.name, ri.customer, ri.date, ri.stuffing, ri.commodity,
		ri.no_invoice, ri.kategori_export, ri.no_do, ri.received_do, ri.carrier,
		ri.pod, ri.party, ri.vessel, ri.etd, ri.open_cy,
		ri.clossing_cy, ri.aju, ri.nopen, ri.date_of_peb, ri.peb, ri.npe,
		ri.packing_list, ri.invoice, ri.date_of_received_npe_fiat, ri.bl_ok,
		ri.pick_up_bl, ri.surrender_bl, ri.date_of_submit_to_pkk, ri.date_of_submit_to_quarantine,
		ri.send_draft_pytho_to_bt, ri.date_of_draft_ok, ri.date_of_issue_pytho
		])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("No Job")+":Link/Rekap Export:130",
		_("Customer")+":Link/Customer:120",
		_("Date")+":Date:100",
		_("Stuffing")+":Date:100",
		_("Commodity")+":Link/Commodity:100",
		_("No Invoice")+"::100",
		_("Kategori Export")+"::100",
		_("No DO")+"::100",
		_("Received DO")+":Datetime:130",
		_("Carrier")+":Link/Supplier:120",
		_("Destination")+":Link/Port:120",
		_("Party")+"::120",
		_("Vessel")+"::140",
		_("ETD")+":Date:100",
		_("Open CY")+":Datetime:130",
		_("Clossing CY")+":Datetime:130",
		_("AJU")+"::120",
		_("Nopen")+"::120",
		_("Date of PEB")+":Date:100",
		_("PEB")+":Datetime:130",
		_("NPE")+":Date:100",
		_("Packing List")+":Date:100",
		_("Invoice")+":Date:100",
		_("Date of Received NPE FIAT")+":Date:100",
		_("BL OK")+":Date:100",
		_("Pick Up BL")+":Date:100",
		_("Surrender BL")+":Date:100",
		_("Date of Submit to PKK")+":Date:100",
		_("Date of Submit to Quarantine")+":Date:100",
		_("Send Draft PYTHO to BT")+":Date:100",
		_("Date of Draft OK")+":Date:100",
		_("Date of Issue PYTHO")+":Date:100",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("daily_report"):
		conditions += " and `daily_report` = '%s'" % frappe.db.escape(filters["daily_report"])

	if filters.get("no_rekap"):
		conditions += " and `name` = '%s'" % frappe.db.escape(filters["no_rekap"])

	if filters.get("customer"):
		conditions += " and `customer` = '%s'" % frappe.db.escape(filters["customer"])

	if filters.get("from_date"):
		conditions += " and date >= '%s'" % frappe.db.escape(filters["from_date"])

	if filters.get("to_date"):
		conditions += " and date <= '%s'" % frappe.db.escape(filters["to_date"])

	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""SELECT daily_report, `name`, customer, `date`, stuffing,
	commodity, no_invoice, kategori_export, no_do, received_do, carrier, pod,
	party, vessel, etd, open_cy, clossing_cy, aju, nopen, date_of_peb,
	peb, npe, packing_list, invoice, date_of_received_npe_fiat, bl_ok,
	pick_up_bl, surrender_bl, date_of_submit_to_pkk, date_of_submit_to_quarantine,
	send_draft_pytho_to_bt, date_of_draft_ok, date_of_issue_pytho
	FROM `tabRekap Export`
	WHERE docstatus != '2' %s
	ORDER BY `name` ASC""" %
		conditions, as_dict=1)
