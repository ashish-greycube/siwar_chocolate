# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "siwar_chocolate"
app_title = "Siwar Chocolate"
app_publisher = "GreyCube Technologies"
app_description = "Customization for Siwar Chocolate"
app_icon = "octicon octicon-gift"
app_color = "brown"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/siwar_chocolate/css/siwar_chocolate.css"
# app_include_js = "/assets/siwar_chocolate/js/siwar_chocolate.js"

# include js, css files in header of web template
# web_include_css = "/assets/siwar_chocolate/css/siwar_chocolate.css"
# web_include_js = "/assets/siwar_chocolate/js/siwar_chocolate.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Company" : "public/js/company.js",
	"Material Request" : "public/js/material_request.js"	
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "siwar_chocolate.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "siwar_chocolate.install.before_install"
# after_install = "siwar_chocolate.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "siwar_chocolate.notifications.get_notification_config"

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
	"Stock Entry": {
		"on_submit": "siwar_chocolate.api.update_client_request_status",
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.update_tray_status"
	],
    "cron": {
        "00 05 * * *": [
            "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.update_tray_status"
        ]
    }	
}


# scheduler_events = {
# 	"all": [
# 		"siwar_chocolate.tasks.all"
# 	],
# 	"daily": [
# 		"siwar_chocolate.tasks.daily"
# 	],
# 	"hourly": [
# 		"siwar_chocolate.tasks.hourly"
# 	],
# 	"weekly": [
# 		"siwar_chocolate.tasks.weekly"
# 	]
# 	"monthly": [
# 		"siwar_chocolate.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "siwar_chocolate.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "siwar_chocolate.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "siwar_chocolate.task.get_dashboard_data"
# }

