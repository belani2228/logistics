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
		ri.validity_do, ri.create_draft_pib, ri.payment_pib, ri.bpom_available,
		ri.spjk, ri.spjm, ri.bahandle, ri.sppb, ri.delivery, ri.kpi, ri.remark])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("NO JOB")+":Link/Rekap Import:150",
		_("NO PO")+"::100",
		_("AJU")+"::100",
		_("COMMODITY")+"::170",
		_("SIZE")+"::150",
		_("ETA")+":Date:100",
		_("DO VALID UNTIL")+":Date:100",
		_("DRAFT PIB")+":Date:100",
		_("PAYMENT PIB")+":Date:100",
		_("BPOM AVAILABLE")+":Date:100",
		_("SPJK")+":Date:100",
		_("SPJM")+":Date:100",
		_("BAHANDLE")+":Date:100",
		_("SPPB")+":Date:100",
		_("DELIVERY")+":Date:100",
		_("KPI (day(s))")+":Float:80",
		_("REMARKS")+"::150",
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
	validity_do, create_draft_pib, payment_pib, bpom_available, spjk, spjm,
	bahandle, sppb, delivery, (delivery - eta) as kpi, remark
	FROM `tabRekap Import`
	WHERE docstatus != '2' %s
	ORDER BY `name` ASC""" %
		conditions, as_dict=1)
