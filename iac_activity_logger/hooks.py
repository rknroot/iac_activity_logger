# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "iac_activity_logger"
app_title = "IAC Activity Logger"
app_publisher = "Eco Data & IAC"
app_description = "Farm Operations Management app for IAC"
app_icon = "fa fa-pagelines"
app_color = "green"
app_email = "rk@whitehatglobal.org"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/iac_activity_logger/css/iac_activity_logger.css"
# app_include_js = "/assets/iac_activity_logger/js/iac_activity_logger.js"

# include js, css files in header of web template
# web_include_css = "/assets/iac_activity_logger/css/iac_activity_logger.css"
# web_include_js = "/assets/iac_activity_logger/js/iac_activity_logger.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "iac_activity_logger/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
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

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "iac_activity_logger.install.before_install"
# after_install = "iac_activity_logger.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "iac_activity_logger.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
    "Tasks": "iac_activity_logger.iac_activity_logger.doctype.tasks.tasks.get_permissions",
    "Farms": "iac_activity_logger.iac_activity_logger.doctype.farms.farms.get_permissions",
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"iac_activity_logger.tasks.all"
# 	],
# 	"daily": [
# 		"iac_activity_logger.tasks.daily"
# 	],
# 	"hourly": [
# 		"iac_activity_logger.tasks.hourly"
# 	],
# 	"weekly": [
# 		"iac_activity_logger.tasks.weekly"
# 	]
# 	"monthly": [
# 		"iac_activity_logger.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "iac_activity_logger.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "iac_activity_logger.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "iac_activity_logger.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

fixtures = ["Workspace", "System Settings", "Role", "Module Profile", "Role Profile", "Workflow", "Workflow State", "Workflow Action Master"]