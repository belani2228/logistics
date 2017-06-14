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
	sinv = doc.name
	for q in doc.quotation_items:
		account = frappe.db.get_value("Item", q.item_code, ["income_account", "description"], as_dict=1)
		siq = frappe.get_doc("Sales Invoice Quotation", q.name)
		siq.income_account = account.income_account
		siq.note = account.description
		siq.save()
	update_sales_invoice_item_print(sinv)

def update_sales_invoice_item_print(sinv):
	sip = frappe.db.sql("""delete from `tabSales Invoice Item Print` where parent = %s""", sinv)
	sii = frappe.db.sql("""select distinct(item_code), item_name, description, item_tax_rate, income_account from `tabSales Invoice Item` where parent = %s and qty >= 1 order by idx asc""", sinv, as_dict=1)
	for u in sii:
		qty = frappe.db.sql("""select sum(qty) from `tabSales Invoice Item` where parent = %s and item_code = %s and qty >= 1""", (sinv, u.item_code))[0][0]
		amount = frappe.db.sql("""select sum(amount) from `tabSales Invoice Item` where parent = %s and item_code = %s and amount >= 1""", (sinv, u.item_code))[0][0]
		rate = amount / qty
		siip = frappe.get_doc({
			"doctype": "Sales Invoice Item Print",
			"parent": sinv,
			"parentfield": "print_items",
			"parenttype": "Sales Invoice",
			"item_code": u.item_code,
			"item_name": u.item_name,
			"description": u.description,
			"item_tax_rate": u.item_tax_rate,
			"qty": qty,
			"rate": rate,
			"amount": amount,
			"base_rate": 0,
			"base_amount": 0,
			"income_account": u.income_account
		})
		siip.insert()

@frappe.whitelist()
def get_items_from_pi(source_name, target_doc=None):
	no_job,rekap = source_name.split("|")

	if target_doc:
		if isinstance(target_doc, basestring):
			import json
			target_doc = frappe.get_doc(json.loads(target_doc))
		target_doc.set("items", [])

	def set_missing_values(source, target):
		target.update_stock = 1
		target.run_method("set_missing_values")

	def update_item(source, target, source_parent):
		if source.selling_rate != 0:
			target.rate = source.selling_rate
			target.amount = source.qty * source.selling_rate

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
						"name":"purchase_invoice_item",
					},
					"postprocess": update_item,
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

# disini script yang hanya dijalankan satu kali
def buat_job_cost():
	insert_job_cost_import()
	insert_job_cost_export()
	update_job_cost_import_items_pinv()
	update_job_cost_import_taxes_pinv()
	update_job_cost_import_items_sinv()
	update_job_cost_import_taxes_sinv()
	update_job_cost_import_sum()

def insert_job_cost_import():
	rekap = frappe.db.sql("""select * from `tabRekap Import` where docstatus != '2'""", as_dict=1)
	for ri in rekap:
		cek_jc = frappe.db.get_value("Job Cost", {"no_job": ri.name}, "name")
		if not cek_jc:
			job_cost = frappe.get_doc({
				"doctype": "Job Cost",
				"no_job": ri.name,
				"jenis_rekap": "Rekap Import",
				"customer": ri.customer,
				"date": ri.date,
				"no_bl": ri.bl_number,
				"party": ri.party
			})
			job_cost.insert()

def insert_job_cost_export():
	rekap = frappe.db.sql("""select * from `tabRekap Export` where docstatus != '2'""", as_dict=1)
	for ri in rekap:
		cek_jc = frappe.db.get_value("Job Cost", {"no_job": ri.name}, "name")
		if not cek_jc:
			job_cost = frappe.get_doc({
				"doctype": "Job Cost",
				"no_job": ri.name,
				"jenis_rekap": "Rekap Export",
				"customer": ri.customer,
				"date": ri.date,
				"no_bl": ri.bl_number,
				"party": ri.party
			})
			job_cost.insert()

def update_job_cost_import_items_pinv():
	jobcost = frappe.db.sql("""select * from `tabJob Cost` where docstatus != '2'""", as_dict=1)
	for jc in jobcost:
		pinv = frappe.db.sql("""select distinct(b.item_code), b.item_name, b.description from `tabPurchase Invoice` a
		inner join `tabPurchase Invoice Item` b on a.`name` = b.parent
 		where a.docstatus = '1' and a.no_job = %s""", jc.no_job, as_dict=1)
		if pinv:
			for b in pinv:
				cek_jc = frappe.db.sql("""select item_code from `tabJob Cost Item` where docstatus != '2' and parent = %s and item_code = %s""", (jc.name, b.item_code))
				sum_pinv_item = frappe.db.sql("""select sum(pii.amount) from `tabPurchase Invoice Item` pii
				inner join `tabPurchase Invoice` pi on pii.parent = pi.`name`
				where pi.docstatus = '1' and pi.no_job = %s and pii.item_code = %s""", (jc.no_job, b.item_code))[0][0]
				if cek_jc:
					jci = frappe.db.get_value("Job Cost Item", {"parent": jc.name, "item_code": b.item_code}, "name")
					job_cost_item = frappe.get_doc("Job Cost Item", jci)
					job_cost_item.cost = sum_pinv_item
					job_cost_item.save()
				else:
					job_cost_item = frappe.get_doc({
						"doctype": "Job Cost Item",
						"parent": jc.name,
						"parentfield": "items",
						"parenttype": "Job Cost",
						"item_code": b.item_code,
						"item_name": b.item_name,
						"description": b.description,
						"cost": sum_pinv_item
					})
					job_cost_item.insert()

def update_job_cost_import_taxes_pinv():
	jobcost = frappe.db.sql("""select * from `tabJob Cost` where docstatus != '2'""", as_dict=1)
	for jc in jobcost:
		pinv = frappe.db.sql("""select distinct(ptc.account_head), ptc.note from `tabPurchase Taxes and Charges` ptc
		inner join `tabPurchase Invoice` pi on ptc.parent = pi.`name`
		where pi.no_job = %s""", jc.no_job, as_dict=1)
		if pinv:
			for b in pinv:
				cek_jc = frappe.db.sql("""select account_head from `tabJob Cost Tax` where docstatus != '2' and parent = %s and account_head = %s""", (jc.name, b.account_head))
				sum_pinv_tax = frappe.db.sql("""select sum(ptc.tax_amount) from `tabPurchase Taxes and Charges` ptc
				inner join `tabPurchase Invoice` pi on ptc.parent = pi.`name`
				where pi.docstatus = '1' and pi.no_job = %s and ptc.account_head = %s""", (jc.no_job, b.account_head))[0][0]
				if cek_jc:
					jct = frappe.db.get_value("Job Cost Tax", {"parent": jc.name, "account_head": b.account_head}, "name")
					job_cost_tax = frappe.get_doc("Job Cost Tax", jct)
					job_cost_tax.cost_tax_amount = sum_pinv_tax
					job_cost_tax.save()
				else:
					job_cost_tax = frappe.get_doc({
						"doctype": "Job Cost Tax",
						"parent": jc.name,
						"parentfield": "taxes",
						"parenttype": "Job Cost",
						"account_head": b.account_head,
						"description": b.note,
						"cost_tax_amount": sum_pinv_tax
					})
					job_cost_tax.insert()

def update_job_cost_import_items_sinv():
	jobcost = frappe.db.sql("""select * from `tabJob Cost` where docstatus != '2'""", as_dict=1)
	for jc in jobcost:
		sinv = frappe.db.sql("""select distinct(b.item_code), b.item_name, b.description from `tabSales Invoice` a
		inner join `tabSales Invoice Item` b on a.`name` = b.parent
 		where a.docstatus = '1' and a.no_job = %s""", jc.no_job, as_dict=1)
		if sinv:
			for b in sinv:
				cek_jc = frappe.db.sql("""select item_code from `tabJob Cost Item` where docstatus != '2' and parent = %s and item_code = %s""", (jc.name, b.item_code))
				sum_sinv_item = frappe.db.sql("""select sum(sii.amount) from `tabSales Invoice Item` sii
				inner join `tabSales Invoice` si on sii.parent = si.`name`
				where si.docstatus = '1' and si.no_job = %s and sii.item_code = %s""", (jc.no_job, b.item_code))[0][0]
				if cek_jc:
					jci = frappe.db.get_value("Job Cost Item", {"parent": jc.name, "item_code": b.item_code}, "name")
					job_cost_item = frappe.get_doc("Job Cost Item", jci)
					job_cost_item.selling = sum_sinv_item
					job_cost_item.save()
				else:
					job_cost_item = frappe.get_doc({
						"doctype": "Job Cost Item",
						"parent": jc.name,
						"parentfield": "items",
						"parenttype": "Job Cost",
						"item_code": b.item_code,
						"item_name": b.item_name,
						"description": b.description,
						"selling": sum_sinv_item
					})
					job_cost_item.insert()

def update_job_cost_import_taxes_sinv():
	jobcost = frappe.db.sql("""select * from `tabJob Cost` where docstatus != '2'""", as_dict=1)
	for jc in jobcost:
		sinv = frappe.db.sql("""select distinct(stc.account_head), stc.note from `tabSales Taxes and Charges` stc
		inner join `tabSales Invoice` si on stc.parent = si.`name`
		where si.no_job = %s""", jc.no_job, as_dict=1)
		if sinv:
			for b in sinv:
				cek_jc = frappe.db.sql("""select account_head from `tabJob Cost Tax` where docstatus != '2' and parent = %s and account_head = %s""", (jc.name, b.account_head))
				sum_sinv_tax = frappe.db.sql("""select sum(stc.tax_amount) from `tabSales Taxes and Charges` stc
				inner join `tabSales Invoice` si on stc.parent = si.`name`
				where si.docstatus = '1' and si.no_job = %s and stc.account_head = %s""", (jc.no_job, b.account_head))[0][0]
				if cek_jc:
					jct = frappe.db.get_value("Job Cost Tax", {"parent": jc.name, "account_head": b.account_head}, "name")
					job_cost_tax = frappe.get_doc("Job Cost Tax", jct)
					job_cost_tax.selling_tax_amount = sum_sinv_tax
					job_cost_tax.save()
				else:
					job_cost_tax = frappe.get_doc({
						"doctype": "Job Cost Tax",
						"parent": jc.name,
						"parentfield": "taxes",
						"parenttype": "Job Cost",
						"account_head": b.account_head,
						"description": b.note,
						"selling_tax_amount": sum_sinv_tax
					})
					job_cost_tax.insert()

def update_job_cost_import_sum():
	jobcost = frappe.db.sql("""select * from `tabJob Cost` where docstatus != '2'""", as_dict=1)
	for jc in jobcost:
		sum_sell_item = frappe.db.sql("""select sum(`selling`) from `tabJob Cost Item` where parent = %s""", jc.name)[0][0]
		sum_sell_tax = frappe.db.sql("""select sum(`selling_tax_amount`) from `tabJob Cost Tax` where parent = %s""", jc.name)[0][0]
		sum_buy_item = frappe.db.sql("""select sum(`cost`) from `tabJob Cost Item` where parent = %s""", jc.name)[0][0]
		sum_buy_tax = frappe.db.sql("""select sum(`cost_tax_amount`) from `tabJob Cost Tax` where parent = %s""", jc.name)[0][0]
		total_selling = flt(sum_sell_item) + flt(sum_sell_tax)
		total_buying = flt(sum_buy_item) + flt(sum_buy_tax)
		profit = flt(total_selling) - flt(total_buying)
		job_cost = frappe.get_doc("Job Cost", jc.name)
		job_cost.total_cost = total_buying
		job_cost.profit_loss = profit
		job_cost.save()

# test
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
