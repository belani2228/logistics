from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def reset_series():
	frappe.db.sql("""UPDATE `tabSeries` SET current = 0 WHERE `name` = 'IMP/PTI'""")

def update_purchase_invoice_detail(doc, method):
	for it in doc.get("items"):
		if it.purchase_invoice:
			doc = frappe.db.sql("""update `tabPurchase Invoice Item` set sales_invoice = %s where `name` = %s""", (it.parent, it.purchase_invoice_item))

def update_purchase_invoice_cancel(doc, method):
	for row in doc.items:
		if row.purchase_invoice:
			doc = frappe.db.sql("""update `tabPurchase Invoice Item` set sales_invoice = null where `name` = %s""", row.purchase_invoice_item)

def update_vendor_trucking_detail(doc, method):
	name = doc.name
	for row in doc.items:
		if row.vendor_trucking_item:
			doc = frappe.db.sql("""UPDATE `tabVendor Trucking Item` SET purchase_invoice = %s, for_print = '0' WHERE `name` = %s""", (name, row.vendor_trucking_item))

def cancel_vendor_trucking_detail(doc, method):
	name = doc.name
	for row in doc.items:
		if row.vendor_trucking_item:
			doc = frappe.db.sql("""UPDATE `tabVendor Trucking Item` SET purchase_invoice = null, for_print = '1' WHERE `name` = %s""", row.vendor_trucking_item)

def update_pi_to_jv(doc, method):
	detail = doc.name
	if not doc.against_jv and doc.purchase_invoice:
		for row in doc.accounts:
			if row.purchase_invoice_item:
				doc = frappe.db.sql("""update `tabPurchase Invoice Item` set journal_entry = %s where `name` = %s""", (detail, row.purchase_invoice_item))
# 	reversing_entry
	elif doc.against_jv and doc.purchase_invoice:
		for row in doc.accounts:
			if row.purchase_invoice_item:
				doc = frappe.db.sql("""update `tabPurchase Invoice Item` set reversing_entry = %s where `name` = %s""", (detail, row.purchase_invoice_item))
				dod = frappe.db.sql("""update `tabJournal Entry Account` set reversing_entry_account = %s where `name` = %s""", (row.name, row.jv_account))

def cancel_pi_to_jv(doc, method):
	if not doc.against_jv and doc.purchase_invoice:
		for row in doc.accounts:
			if row.purchase_invoice_item:
				doc = frappe.db.sql("""update `tabPurchase Invoice Item` set journal_entry = NULL where `name` = %s""", row.purchase_invoice_item)
# 	reversing_entry
	elif doc.against_jv and doc.purchase_invoice:
		for row in doc.accounts:
			if row.purchase_invoice_item:
				doc = frappe.db.sql("""update `tabPurchase Invoice Item` set reversing_entry = NULL where `name` = %s""", row.purchase_invoice_item)
				dod = frappe.db.sql("""update `tabJournal Entry Account` set reversing_entry_account = NULL where `name` = %s""", row.jv_account)

def update_si_quotation(doc, method):
	for q in doc.quotation_items:
		account = frappe.db.get_value("Item", q.item_code, ["income_account", "description"], as_dict=1)
		siq = frappe.get_doc("Sales Invoice Quotation", q.name)
		siq.income_account = account.income_account
		siq.note = account.description
		siq.save()

@frappe.whitelist()
def get_items_from_pi(source_name, target_doc=None):
	no_job,rekap = source_name.split("|")

	if target_doc:
		if isinstance(target_doc, basestring):
			import json
			target_doc = frappe.get_doc(json.loads(target_doc))

	def set_missing_values(source, target):
		target.update_stock = 1
		target.run_method("set_missing_values")

	query = frappe.db.sql_list("""SELECT dn.`name`
		FROM `tabPurchase Invoice` dn
		WHERE dn.no_job = %s AND dn.docstatus != '2' ORDER BY dn.`name` ASC""", no_job)

	si = get_mapped_doc(rekap, no_job, {
		rekap: {
			"doctype": "Sales Invoice",
		},
	}, target_doc)
	for q in query:
		si = get_mapped_doc("Purchase Invoice", q, {
				"Purchase Invoice": {
					"doctype": "Sales Invoice",
					"field_no_map": [
						"base_total", "base_net_total", "net_total", "total",
						"base_grand_total", "grand_total"
					],
				},
				"Purchase Invoice Item": {
					"doctype": "Sales Invoice Item",
					"field_map": {
						"parent": "purchase_invoice",
						"name":"purchase_invoice_item"
					},
					"condition":lambda doc: doc.sales_invoice is None
				},
			}, target_doc, set_missing_values)

	return si

@frappe.whitelist()
def make_journal_entry(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.purchase_invoice = source_name
		target.run_method("set_missing_values")

	def update_item(source, target, source_parent):
		target.purchase_invoice = source_name

	doc = get_mapped_doc("Purchase Invoice", source_name, {
		"Purchase Invoice": {
			"doctype": "Journal Entry",
			"validation": {
				"docstatus": ["=", 1],
			},
		},
		"Purchase Invoice Item": {
			"doctype": "Journal Entry Account",
			"field_map": {
				"expense_account": "account",
				"net_amount": "credit_in_account_currency",
				"name": "purchase_invoice_item"
			},
			"postprocess": update_item,
			"condition":lambda doc: doc.journal_entry is None
		},
	}, target_doc, set_missing_values)
	return doc

@frappe.whitelist()
def make_reversing_entry(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.run_method("set_missing_values")

	doc = get_mapped_doc("Journal Entry", source_name, {
		"Journal Entry": {
			"doctype": "Journal Entry",
			"field_map":{
				"name": "against_jv",
			},
			"validation": {
				"docstatus": ["=", 1],
			},
		},
		"Journal Entry Account": {
			"doctype": "Journal Entry Account",
			"field_map": {
				"credit_in_account_currency": "debit_in_account_currency",
				"debit_in_account_currency": "credit_in_account_currency",
				"name": "jv_account"
			},
			"condition":lambda doc: doc.reversing_entry_account is None
		},
	}, target_doc, set_missing_values)
	return doc

@frappe.whitelist()
def get_items_from_quotation(source_name, target_doc=None):
	if target_doc:
		if isinstance(target_doc, basestring):
			import json
			target_doc = frappe.get_doc(json.loads(target_doc))
		target_doc.set("quotation_items", [])

	doclist = get_mapped_doc("Quotation", source_name, {
		"Quotation": {
			"doctype": "Sales Invoice",
			"field_no_map":["customer", "posting_date", "due_date", "items"]
		},
		"Quotation Item": {
			"doctype": "Sales Invoice Quotation",
			"field_map":{
				"amount": "amount_siq"
			}
		},
	}, target_doc)
	return doclist

@frappe.whitelist()
def get_items_si_qoute(source_name, target_doc=None):
	if target_doc:
		if isinstance(target_doc, basestring):
			import json
			target_doc = frappe.get_doc(json.loads(target_doc))
		target_doc.set("items", [])

	doclist = get_mapped_doc("Sales Invoice", source_name, {
		"Sales Invoice": {
			"doctype": "Sales Invoice",
			"field_no_map":["customer", "posting_date", "due_date", "items"]
		},
		"Sales Invoice Quotation": {
			"doctype": "Sales Invoice Item",
			"field_map":{
				"amount_siq": "amount",
				"note": "description"
			},
			"condition":lambda doc: doc.check == 1
		},
	}, target_doc)
	return doclist

def coba_doang():
	tampung = []
	query = frappe.get_all("Purchase Invoice",
		fields=["name"],
		filters=[["docstatus", "!=", 2]],
		order_by='name asc')

	for q in query:
		tampung.append(q["name"])

	temp = ', '.join(tampung)
	frappe.throw(temp)
