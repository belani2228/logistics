# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _
from . import __version__ as app_version

app_name = "logistics"
app_title = "Logistics"
app_publisher = "Abcgroups"
app_description = "App for managing documents logistics"
app_icon = "octicon octicon-clippy"
app_color = "#A531C6"
app_email = "develop@ridhosribumi.com"
app_license = "GNU General Public License"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "assets/css/custom.css"
# app_include_js = "/assets/logistics/js/logistics.js"

# include js, css files in header of web template
# web_include_css = "/assets/logistics/css/logistics.css"
# web_include_js = "/assets/logistics/js/logistics.js"

# Home Pages
# ----------
website_context = {
	"splash_image": "/files/splash-rss.png"
}

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "logistics.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "logistics.install.before_install"
# after_install = "logistics.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "logistics.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Purchase Invoice": {
		"on_submit": "logistics.logistics.lemparan.update_deposite_note_detail",
		"before_cancel": "logistics.logistics.lemparan.update_deposite_note_cancel"
	},
	"Sales Invoice": {
		"on_submit": "logistics.logistics.lemparan.update_purchase_invoice_detail",
		"before_cancel": "logistics.logistics.lemparan.update_purchase_invoice_cancel"
	},
	"Rekap Import": {
		"on_update": "logistics.logistics.lemparan.update_party_import"
	},
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"logistics.tasks.all"
# 	],
# 	"daily": [
# 		"logistics.tasks.daily"
# 	],
# 	"hourly": [
#        "logistics.logistics.lemparan.reset_series"
# 	],
# 	"weekly": [
# 		"logistics.tasks.weekly"
# 	]
# 	"monthly": [
# 		"logistics.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "logistics.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "logistics.event.get_events"
# }
