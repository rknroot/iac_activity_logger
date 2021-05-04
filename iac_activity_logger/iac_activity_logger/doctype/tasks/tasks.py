# -*- coding: utf-8 -*-
# Copyright (c) 2021, Eco Data & IAC and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, cstr, getdate
import calendar
from frappe import _
from six.moves import range
from six import string_types
import json
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from frappe.utils.user import get_enabled_system_users
from frappe.desk.reportview import get_filters_cond
from datetime import date, time, datetime, timedelta
from frappe.model.naming import make_autoname, parse_naming_series

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

class Tasks(Document):
	def onload(self):
		if self.create_recurrence_task:
			parent_tasks = frappe.db.get_all("Tasks",filters={"parent_tasks":self.name},fields=('name','task_date','status', 'repeat_on'))
			for i in parent_tasks:
				if i.name not in [j.title for j in self.get("child_tasks")]:
					child = self.append('child_tasks',{})
					child.title = i.name
					child.status = i.status
					child.task_date = i.task_date
					child.repeat_on = i.repeat_on

	def autoname(self):
		task_series = frappe.db.get_single_value("Tasks Settings","tasks_series")
		if not task_series:
			frappe.throw("Tasks Series is not created in settings, Contact Admin")
		if not self.parent_tasks:
			self.name = make_autoname(task_series)
		if self.parent_tasks:
			self.name = make_autoname(self.parent_tasks + '.-.##')


@frappe.whitelist()
def get_tasks(start, end, user=None, for_reminder=False, filters=None):
	if isinstance(filters, string_types):
		filters = json.loads(filters)

	filter_condition = get_filters_cond('Tasks', filters, [])
	tables = ["`tabTasks`"]

	events = frappe.db.sql("""
		SELECT `tabTasks`.name,
				`tabTasks`.task_date,
                `tabTasks`.task_title,
				`tabTasks`.priority,
				`tabTasks`.description,
				`tabTasks`.owner,
				`tabTasks`.create_recurrence_task,
				`tabTasks`.repeat_on,
				`tabTasks`.repeat_till,
				`tabTasks`.monday,
				`tabTasks`.tuesday,
				`tabTasks`.wednesday,
				`tabTasks`.thursday,
				`tabTasks`.friday,
				`tabTasks`.saturday,
				`tabTasks`.sunday,
				`tabTasks`.parent_tasks
		FROM {tables}
		WHERE (
				(
					(date(`tabTasks`.task_date) BETWEEN date(%(start)s) AND date(%(end)s))
					OR (date(`tabTasks`.task_date) BETWEEN date(%(start)s) AND date(%(end)s))
					OR (
						date(`tabTasks`.task_date) <= date(%(start)s)
						AND date(`tabTasks`.task_date) >= date(%(end)s)
					)
				)
				AND (
					date(`tabTasks`.task_date) <= date(%(start)s)
					OR date(`tabTasks`.task_date) = date(%(start)s)
					AND `tabTasks`.create_recurrence_task=1
					AND coalesce(`tabTasks`.repeat_till, '3000-01-01') > date(%(start)s)
					AND `tabTasks`.name = (%(user)s)
				)
			)
		{filter_condition}
		ORDER BY `tabTasks`.task_date""".format(
			tables=", ".join(tables),
			filter_condition=filter_condition
		), {
			"start": start,
			"end": end,
			"user": user,
		}, as_dict=1)


	# process recurring events
	start = start.split(" ")[0]
	end = end.split(" ")[0]
	add_events = []
	remove_events = []

	def add_event(e, date):
		#frappe.msgprint("Add"+(str(e))+ "dat" + str(date))
		new_event = e.copy()
		enddate = add_days(date,int(date_diff(e.task_date.split(" ")[0], e.task_date.split(" ")[0]))) \
			if (e.task_date and e.task_date) else date
		new_event.task_date = date + " " + e.task_date.split(" ")[1]
		new_event.task_date = new_event.task_date = enddate + " " + e.task_date.split(" ")[1] if e.task_date else None
		add_events.append(new_event)

	for e in events:
		if e.create_recurrence_task:
			e.task_date = get_datetime_str(e.task_date)
			e.task_date = get_datetime_str(e.task_date) if e.task_date else None

			event_start, time_str = get_datetime_str(e.task_date).split(" ")

			repeat = "3000-01-01" if cstr(e.repeat_till) == "" else e.repeat_till

			if e.repeat_on == "Yearly":
				start_year = cint(start.split("-")[0])
				end_year = cint(end.split("-")[0])

				# creates a string with date (27) and month (07) eg: 07-27
				event_start = "-".join(event_start.split("-")[1:])

				# repeat for all years in period
				for year in range(start_year, end_year+1):
					date = str(year) + "-" + event_start
					if getdate(date) >= getdate(start) and getdate(date) <= getdate(end) and getdate(date) <= getdate(repeat):
						add_event(e, date)

				remove_events.append(e)

			if e.repeat_on == "Monthly":
				# creates a string with date (27) and month (07) and year (2019) eg: 2019-07-27
				date = start.split("-")[0] + "-" + start.split("-")[1] + "-" + event_start.split("-")[2]

				# last day of month issue, start from prev month!
				try:
					getdate(date)
				except ValueError:
					date = date.split("-")
					date = date[0] + "-" + str(cint(date[1]) - 1) + "-" + date[2]

				start_from = date
				for i in range(int(date_diff(end, start) / 30) + 3):
					if getdate(date) >= getdate(start) and getdate(date) <= getdate(end) \
						and getdate(date) <= getdate(repeat) and getdate(date) >= getdate(event_start):
						add_event(e, date)
					date = add_months(start_from, i+1)
				remove_events.append(e)

			if e.repeat_on == "Weekly":
				for cnt in range(date_diff(end, start) + 1):
					date = add_days(start, cnt)
					if getdate(date) >= getdate(start) and getdate(date) <= getdate(end) \
						and getdate(date) <= getdate(repeat) and getdate(date) >= getdate(event_start) \
						and e[weekdays[getdate(date).weekday()]]:
						add_event(e, date)
				remove_events.append(e)

			if e.repeat_on == "Daily":
				for cnt in range(date_diff(end, start) + 1):
					date = add_days(start, cnt)
					if getdate(date) >= getdate(event_start) and getdate(date) <= getdate(end) and getdate(date) <= getdate(repeat):
						add_event(e, date)
				remove_events.append(e)
	for e in remove_events:
		events.remove(e)

	get_date_list = frappe.db.sql(""" select task_date from `tabTasks` where parent_tasks = %s""", e.name, as_dict = 1)
	for j in get_date_list:
		for k in add_events:
			if j.task_date == getdate(k.task_date):
				add_events.remove(k)

	events = events + add_events
	for e in events:
		task_schedule = frappe.new_doc("Tasks")
		task_schedule.task_title = e.task_title
		task_schedule.priority = e.priority
		task_schedule.description = e.description
		task_schedule.task_date = e.task_date
		task_schedule.parent_tasks = e.name
		task_schedule.repeat_on = e.repeat_on
		task_schedule.flags.ignore_permissions = 1
		task_schedule.insert()

	#return events

@frappe.whitelist()
def delete_tasks(start, end, user=None, for_reminder=False, filters=None):
		"""Delete all schedule within the Date range and specified filters"""
		self = frappe.get_doc("Tasks", user)
		rescheduled = []
		reschedule_errors = []
		schedules = frappe.get_list("Tasks",
			fields=["name", "task_date", "repeat_on"],
			filters=[
				["task_title", "=", self.task_title],
				["status", "=", "New"],
				["task_date", ">=", self.repeat_till]
			]
		)
		if schedules:
			for d in schedules:
				frappe.db.sql("""delete from `tabChild Tasks` where title = %s and task_date = %s""", (d.name, d.task_date))
				frappe.db.sql("""delete from `tabTasks` where name = %s""", (d.name))
		else:
			get_tasks(start, end, user=None, for_reminder=False, filters=None)
			del_duplicate(start)

@frappe.whitelist()
def delete_tasks_repeat(start, end, user=None, for_reminder=False, filters=None):
		"""Delete all schedule within the Date range and specified filters"""
		self = frappe.get_doc("Tasks", user)
		rescheduled = []
		reschedule_errors = []
		schedules = frappe.get_list("Tasks",
			fields=["name", "task_date", "repeat_on"],
			filters=[
				["task_title", "=", self.task_title],
				["status", "=", "New"],
				["create_recurrence_task", "=", "0"],
				["task_date", "<=", self.repeat_till]
			]
		)
		if schedules:
			for d in schedules:
				frappe.db.sql("""delete from `tabChild Tasks` where parent = %s and task_date = %s """, (d.name, d.task_date))
				frappe.db.sql("""delete from `tabTasks` where name = %s""", (d.name))
		else:
			get_tasks(start, end, user=None, for_reminder=False, filters=None)
			del_duplicate(start)

@frappe.whitelist()
def del_duplicate(start):
	get_tasks_duplicate = frappe.db.sql("""select name, task_date, create_recurrence_task from `tabTasks` where task_date = %s""",(start),as_dict=1)
	for i in get_tasks_duplicate:
		if i.create_recurrence_task == 0:
			frappe.db.sql("""delete from `tabTasks` where name = %s""",(i.name))

@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Course Schedule Calendar view rendering.
	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions("Tasks", filters)

	data = frappe.db.sql("""select name, status, task_title,
			timestamp(task_date, time) as from_datetime,
			timestamp(task_date, time) as to_datetime,
			0 as 'allDay'
		from `tabTasks`
		where ( task_date between %(start)s and %(end)s )
		{conditions}""".format(conditions=conditions), {
			"start": start,
			"end": end
			}, as_dict=True, update={"allDay": 0})

	return data


@frappe.whitelist()
def get_permissions(user):
	retval = ''
	if "System Manager" in frappe.permissions.get_roles(frappe.session.user):
		pass
	elif "Farm Supervisor" in frappe.permissions.get_roles(frappe.session.user):
		retval = """((`tabTasks`.assigned_to = '{user}'))""".format(user=frappe.session.user)
	return retval