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
		data.append([ri.name, ri.po_no, ri.aju, ri.commodity, ri.party, ri.eta,
		ri.validity_do, ri.receive_copy_document, ri.create_draft_pib, ri.payment_pib, ri.bpom_available,
		ri.response_qua, ri.spjk, ri.spjm, ri.bahandle, ri.sppb, ri.delivery, ri.kpi, ri.remark])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("No Job")+":Link/Rekap Import:150",
		_("No PO")+"::100",
		_("AJU")+"::100",
		_("Commodity")+"::170",
		_("Size")+"::150",
		_("ETA")+":Date:100",
		_("Tgl Valid DO")+":Date:100",
		_("HANDOVER DOC TO PATRINDO")+":Date:100",
		_("Tgl Draft PIB")+":Date:100",
		_("Tgl Payment PIB")+":Date:100",
		_("Tgl BPOM Available")+":Date:100",
		_("Tgl Quarantine")+":Date:100",
		_("Tgl SPJK")+":Date:100",
		_("Tgl SPJM")+":Date:100",
		_("Tgl BAHANDLE")+":Date:100",
		_("Tgl SPPB")+":Date:100",
		_("Tgl Delivery")+":Date:100",
		_("KPI")+"::80",
		_("Remarks")+"::150",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("customer"):
		conditions += " and customer = '%s'" % frappe.db.escape(filters["customer"])
	if filters.get("from_date"):
		conditions += " and date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and date <= '%s'" % frappe.db.escape(filters["to_date"])
	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""SELECT name, po_no, aju, commodity, party, eta,
	validity_do, receive_copy_document, create_draft_pib, payment_pib, bpom_available,
	response_qua, spjk, spjm,	bahandle, sppb, delivery,
	if(delivery - eta = 1, CONCAT(delivery - eta, " day"), CONCAT(delivery - eta, " days")) as kpi,
	remark
	FROM `tabRekap Import`
	WHERE docstatus != '2' %s
	ORDER BY `name` ASC""" %
		conditions, as_dict=1)
