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
		data.append([ri.name, ri.customer, ri.aju, ri.commodity, ri.eta,
		ri.receive_copy_document, ri.receive_ori_document, ri.pick_up_do,
		ri.tt_do, ri.bpom_available, ri.tt_ski, ri.response_qua, ri.tt_quarantine,
		ri.payment_pib, ri.response, ri.doc_complete
	])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("No Job")+":Link/Rekap Import:150",
		_("Customer")+":Link/Customer:150",
		_("AJU")+"::100",
		_("Commodity")+"::100",
		_("ETA")+":Date:90",
		_("Tgl Receive Copy Doc")+":Date:130",
		_("Tgl Receive Ori Doc")+":Date:120",
		_("Tgl Pick Up DO")+":Date:100",
		_("TT DO")+":Float:80",
		_("Tgl Issued SKI")+":Date:100",
		_("TT SKI")+":Float:80",
		_("Tgl Issued Quarantine")+":Date:130",
		_("TT Quarantine")+":Float:90",
		_("Tgl Payment PIB")+":Date:100",
		_("Tgl Response")+":Date:100",
		_("Doc Complete")+":Float:100",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("no_job"):
		conditions += " and `name` = '%s'" % frappe.db.escape(filters["no_job"])
	if filters.get("customer"):
		conditions += " and customer = '%s'" % frappe.db.escape(filters["customer"])

	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""SELECT `name`, customer, aju, commodity, eta,
	receive_copy_document, receive_ori_document, pick_up_do,
	if(eta > receive_ori_document, pick_up_do - eta, pick_up_do - receive_ori_document) as tt_do,
	bpom_available, (bpom_available - receive_copy_document) as tt_ski, response_qua,
	(response_qua - receive_ori_document) as tt_quarantine,	payment_pib, response,
	CASE
		WHEN(response_qua >= bpom_available or response_qua >= receive_ori_document or response_qua >= eta or response_qua >= payment_pib)
			THEN response - response_qua
		WHEN(bpom_available >= response_qua or bpom_available >= receive_ori_document or bpom_available >= eta or bpom_available >= payment_pib)
			THEN response - bpom_available
		WHEN(receive_ori_document >= bpom_available or receive_ori_document >= response_qua or receive_ori_document >= eta or receive_ori_document >= payment_pib)
			THEN response - receive_ori_document
		WHEN(eta >= bpom_available or eta >= receive_ori_document or eta >= response_qua or eta >= payment_pib)
			THEN response - eta
		WHEN(payment_pib >= bpom_available or payment_pib >= receive_ori_document or payment_pib >= eta or payment_pib >= response_qua)
			THEN response - payment_pib
	END AS doc_complete
	FROM `tabRekap Import`
	WHERE docstatus != '2' %s
	ORDER BY `name` ASC""" %
		conditions, as_dict=1)
