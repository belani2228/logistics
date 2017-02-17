# Copyright (c) 2013, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	#columns, data = [], []
	#return columns, data
	columns = get_columns()
	sl_entries = get_entries(filters)
	data = []

	for ri in sl_entries:
		data.append([ri.name,
			ri.po_no,
			ri.aju,
			ri.eta,
			ri.customer,
			ri.commodity,
			ri.qty,
			ri.size_cont,
			ri.type,
			ri.daftar_container,
			ri.bl_number,
			ri.vessel_name,
			ri.shipper,
			ri.pol,
			ri.pod,
			ri.carrier,
			ri.ftd,
			ri.receive_copy_document,
			ri.create_draft_pib,
			ri.send_raft_pib_to_cnee,
			ri.cfm_draft_pib,
			ri.print_original_pib,
			ri.payment_pib,
			ri.val_pib,
			ri.input_data_bpom,
			ri.receive_original_leter_poa,
			ri.send_original_doc_to_bpom,
			ri.response_recom_bpom_oke,
			ri.response_recom_bpom_reject,
			ri.bpom_available,
			ri.pickup_bpom,
			ri.receive_original_letter_poa,
			ri.input_doc_data_qua,
			ri.response_qua,
			ri.complete_letter_qua,
			ri.receive_original_doc_from_qua,
			ri.pick_up_do,
			ri.extend_do,
			ri.do_duration,
			ri.send_data_to_custom,
			ri.reject,
			ri.request_dnp_tt,
			ri.receive_tt,
			ri.send_dnp_tt,
			ri.notul,
			ri.pay_notul,
			ri.create_letter_obj,
			ri.send_letter_obj,
			ri.analyzing,
			ri.spjk,
			ri.spjm,
			ri.express,
			ri.bahandle,
			ri.sppb,
			ri.ob,
			ri.delivery,
			ri.out_warehouse,
			ri.arrive_depo,
			ri.remark])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("No Job")+":Link/Task:110",
		_("PO No")+"::100",
		_("AJU")+"::100",
		_("ETA")+":Date:100",
		_("Customer")+":Link/Customer:170",
		_("Commodity")+"::100",
		_("Qty")+":Float:50",
		_("Size")+"::50",
		_("Type")+"::50",
		_("No Container")+"::120",
		_("BL Number")+"::120",
		_("Vessel Name")+"::120",
		_("Shipper")+"::120",
		_("POL")+"::120",
		_("POD")+"::120",
		_("Carrier")+"::100",
		_("FTD")+"::90",
		_("Receive Copy Document")+":Date:90",
		_("Crate Draft PIB")+":Date:90",
		_("Send Draft PIB to CNEE")+":Date:90",
		_("CFM Draft PIB")+":Date:90",
		_("Print Original PIB")+":Date:90",
		_("Payment PIB")+":Date:90",
		_("VAL PIB")+":Date:90",
		_("Input data BPOM/SRB3")+":Date:90",
		_("Receive Original Leter POA (BPOM/SPB3)")+":Date:90",
		_("Send Original Doc to BPOM/KLH")+":Date:90",
		_("Response Recom BPOM (OKE)")+":Date:90",
		_("Response Recom BPOM (REJECT)")+":Date:90",
		_("BPOM Available")+":Date:90",
		_("Pick up BPOM")+":Date:90",
		_("Receive Original letter POA (QUA)")+":Date:90",
		_("Input doc & data QUA")+":Date:90",
		_("Response QUA")+":Date:90",
		_("Complete Letter QUA")+":Date:90",
		_("Receive Original Doc from QUA")+":Date:90",
		_("Pick up DO")+":Date:90",
		_("Extend DO")+":Date:90",
		_("DO Duration")+"::90",
		_("Send Data to Custom")+":Date:90",
		_("Reject")+":Date:90",
		_("Request DNP & TT")+":Date:90",
		_("Receive TT")+":Date:90",
		_("Send DNP & TT")+":Date:90",
		_("Notul")+":Date:90",
		_("Pay Notul")+":Date:90",
		_("Create Letter OBJ")+":Date:90",
		_("Send Letter OBJ")+":Date:90",
		_("Analyzing")+":Date:90",
		_("SPJK")+":Date:90",
		_("SPJM")+":Date:90",
		_("Express")+":Date:90",
		_("Bahandle (Hi-Co)")+":Date:90",
		_("SPPB")+":Date:90",
		_("OB")+":Date:90",
		_("Delivery")+":Date:90",
		_("Out Warehouse")+":Date:90",
		_("Delivery")+":Date:90",
		_("Arrive Depo")+":Date:90",
		_("Remark")+"::200",
	]

	return columns

def get_conditions(filters):
	conditions = ""
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
	return frappe.db.sql("""SELECT `name`, po_no, aju, eta, customer, commodity,
	qty, size_cont, type, daftar_container, bl_number, vessel_name, shipper, pol,
	pod, carrier, ftd, receive_copy_document, create_draft_pib, send_draft_pib_to_cnee,
	cfm_draft_pib, print_original_pib, payment_pib, val_pib, input_data_bpom,
	receive_original_leter_poa, send_original_doc_to_bpom, response_recom_bpom_oke,
	response_recom_bpom_reject, bpom_available, pickup_bpom, receive_original_letter_poa,
	input_doc_data_qua, response_qua, complete_letter_qua, receive_original_doc_from_qua,
	pick_up_do, extend_do, do_duration, send_data_to_custom, reject, request_dnp_tt,
	receive_tt, send_dnp_tt, notul, pay_notul, create_letter_obj, send_letter_obj,
	analyzing, spjk, spjm, express, bahandle, sppb, ob, delivery, out_warehouse,
	arrive_depo, remark
	FROM `tabRekap Import`
	WHERE docstatus != '2' %s
	ORDER BY `name` ASC""" %
		conditions, as_dict=1)
