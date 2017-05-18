from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def reset_series():
	frappe.db.sql("""UPDATE `tabSeries` SET current = 0 WHERE `name` = 'IMP/PTI'""")

def update_deposite_note_detail(doc, method):
	args = doc.deposite_note
	name = doc.name
	no_rekap = doc.no_job
	for row in doc.items:
		if row.deposite_note_detail:
			doc = frappe.db.sql("""UPDATE `tabDeposite Note Item` SET pi_no = %s
			WHERE `name` = %s""", (name, row.deposite_note_detail))

	return update_deposite_note(args)

def update_job_cost_detail(doc, method):
	jc = frappe.db.get_value("Job Cost", {"no_job": doc.no_job}, "name")
	args = jc
	for row in doc.items:
		jci = frappe.db.get_value("Job Cost Item", {"parent": jc, "item_code": row.item_code}, "name")
		if jci:
			job_cost_item = frappe.get_doc("Job Cost Item", jci)
			if row.parenttype == "Purchase Invoice":
				cost = frappe.db.get_value("Job Cost Item", jci, "cost")
				cost += row.amount
				job_cost_item.cost = cost
			else:
				sell = frappe.db.get_value("Job Cost Item", jci, "selling")
				sell += row.amount
				job_cost_item.selling = sell
			job_cost_item.save()
		else:
			if row.parenttype == "Purchase Invoice":
				job_cost_item = frappe.get_doc({
					"doctype": "Job Cost Item",
					"parent": jc,
					"parentfield": "items",
					"parenttype": "Job Cost",
					"item_code": row.item_code,
					"item_name": row.item_name,
					"description": row.description,
					"cost": row.amount
				})
			else:
				job_cost_item = frappe.get_doc({
					"doctype": "Job Cost Item",
					"parent": jc,
					"parentfield": "items",
					"parenttype": "Job Cost",
					"item_code": row.item_code,
					"item_name": row.item_name,
					"description": row.description,
					"selling": row.amount
				})
			job_cost_item.insert()
	for tax in doc.taxes:
		jct = frappe.db.get_value("Job Cost Tax", {"parent": jc, "account_head": tax.account_head}, "name")
		if jct:
			job_cost_tax = frappe.get_doc("Job Cost Tax", jct)
			if tax.parenttype == "Purchase Invoice":
				cost = frappe.db.get_value("Job Cost Tax", jct, "cost_tax_amount")
				cost += tax.tax_amount
				job_cost_tax.cost_tax_amount = cost
			else:
				sell = frappe.db.get_value("Job Cost Tax", jct, "selling_tax_amount")
				sell += tax.tax_amount
				job_cost_tax.cost_tax_amount = cost
			job_cost_tax.save()
		else:
			if tax.parenttype == "Purchase Invoice":
				job_cost_tax = frappe.get_doc({
					"doctype": "Job Cost Tax",
					"parent": jc,
					"parentfield": "taxes",
					"parenttype": "Job Cost",
					"account_head": tax.account_head,
					"description": tax.description,
					"cost_tax_amount": tax.tax_amount
				})
			else:
				job_cost_tax = frappe.get_doc({
					"doctype": "Job Cost Tax",
					"parent": jc,
					"parentfield": "taxes",
					"parenttype": "Job Cost",
					"account_head": tax.account_head,
					"description": tax.description,
					"selling_tax_amount": tax.tax_amount
				})
			job_cost_tax.insert()
	return update_job_cost(args)

def update_deposite_note_cancel(doc, method):
	args = doc.deposite_note
	for row in doc.items:
		if row.deposite_note_detail:
			doc = frappe.db.sql("""UPDATE `tabDeposite Note Item` SET pi_no = NULL
			WHERE `name` = %s""", (row.deposite_note_detail))

	return update_deposite_note(args)

def cancel_job_cost_detail(doc, method):
	jc = frappe.db.get_value("Job Cost", {"no_job": doc.no_job}, "name")
	for row in doc.items:
		jci = frappe.db.get_value("Job Cost Item", {"parent": jc, "item_code": row.item_code}, "name")
		if jci:
			cost = frappe.db.get_value("Job Cost Item", jci, "cost")
			sell = frappe.db.get_value("Job Cost Item", jci, "selling")
			job_cost_item = frappe.get_doc("Job Cost Item", jci)
			if row.parenttype == "Purchase Invoice":
				cost = cost - row.amount
				job_cost_item.cost = cost
			else:
				sell = sell - row.amount
				job_cost_item.selling = sell
			job_cost_item.save()
			cost = frappe.db.get_value("Job Cost Item", jci, "cost")
			sell = frappe.db.get_value("Job Cost Item", jci, "selling")
			if cost == 0 and sell == 0:
				job_cost_item = frappe.get_doc("Job Cost Item", jci)
				job_cost_item.delete()
	for tax in doc.taxes:
		jct = frappe.db.get_value("Job Cost Tax", {"parent": jc, "account_head": tax.account_head}, "name")
		if jct:
			tax_cost = frappe.db.get_value("Job Cost Tax", jct, "cost_tax_amount")
			tax_sell = frappe.db.get_value("Job Cost Tax", jct, "selling_tax_amount")
			job_cost_tax = frappe.get_doc("Job Cost Tax", jct)
			if tax.parenttype == "Purchase Invoice":
				tax_cost = tax_cost - tax.tax_amount
				job_cost_tax.cost_tax_amount = tax_cost
			else:
				tax_sell = tax_sell - tax.tax_amount
				job_cost_tax.selling_tax_amount = tax_sell
			job_cost_tax.save()
			tax_cost = frappe.db.get_value("Job Cost Tax", jct, "cost_tax_amount")
			tax_sell = frappe.db.get_value("Job Cost Tax", jct, "selling_tax_amount")
			if tax_cost == 0 and tax_sell == 0:
				job_cost_tax = frappe.get_doc("Job Cost Tax", jct)
				job_cost_tax.delete()
	args = jc
	return update_job_cost(args)

def update_deposite_note(args):
	a2 = frappe.db.sql_list("""SELECT COUNT(`name`) FROM `tabDeposite Note Item`
		WHERE parent = %s AND pi_no IS NOT NULL""", args)

	frappe.db.sql("""UPDATE `tabDeposite Note` SET terpakai = %s WHERE `name` = %s""", (a2, args))

def update_purchase_invoice_detail(doc, method):
	for row in doc.items:
		if row.purchase_invoice:
			doc = frappe.db.sql("""UPDATE `tabPurchase Invoice Item` SET sales_invoice = %s
			WHERE `name` = %s""", (row.parent, row.purchase_invoice_item))

def update_purchase_invoice_cancel(doc, method):
	for row in doc.items:
		if row.purchase_invoice:
			doc = frappe.db.sql("""UPDATE `tabPurchase Invoice Item` SET sales_invoice = NULL
			WHERE `name` = %s""", row.purchase_invoice_item)

def update_job_cost(args):
	count1 = frappe.db.get_value("Job Cost Item", {"parent": args}, "name")
	if count1:
		jmlh_cost = frappe.db.sql("""select sum(cost) from `tabJob Cost Item` where parent = %s""", args)[0][0]
		jmlh_sell = frappe.db.sql("""select sum(selling) from `tabJob Cost Item` where parent = %s""", args)[0][0]
#	count2 = frappe.db.get_value("Job Cost Tax", {"parent": args}, "name")
#	if count2:
		jmlh_cost_tax = frappe.db.sql("""select sum(cost_tax_amount) from `tabJob Cost Tax` where parent = %s""", args)[0][0]
		jmlh_sell_tax = frappe.db.sql("""select sum(selling_tax_amount) from `tabJob Cost Tax` where parent = %s""", args)[0][0]
		sum_cost = flt(jmlh_cost) + flt(jmlh_cost_tax)
		sum_sell = flt(jmlh_sell) + flt(jmlh_sell_tax)
		profit = flt(sum_sell) - flt(sum_cost)
#	else:
#		sum_cost = str(jmlh_cost)
#		sum_sell = str(jmlh_sell)
	else:
		sum_cost = 0
		sum_sell = 0
		profit = 0

#	msgprint("total cost: "+str(jmlh_cost))
	frappe.db.sql("""UPDATE `tabJob Cost` SET total_cost = %s, total_selling = %s, profit_loss = %s WHERE `name` = %s""", (sum_cost, sum_sell, profit, args))

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
#		pi = frappe.db.get_value("Purchase Invoice", {"for_print":1, "parent":no_doc}, ["jenis_rekap", "no_job"], as_dict=1)
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
