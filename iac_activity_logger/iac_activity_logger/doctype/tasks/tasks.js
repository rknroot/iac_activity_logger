// Copyright (c) 2021, Eco Data & IAC and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tasks', {
	// refresh: function(frm) {

	// }
	setup: function(frm) {
		frm.set_query("assigned_to", function() {
				return {
						filters: {'role_profile_name': "farm supervisor"}
				}
		});
	},
	refresh(frm)
	{
		$(cur_frm.fields_dict.create_tasks.input).addClass("btn-primary").css({'color':'white','font-weight': 'bold'});
		$(cur_frm.fields_dict.reschedule_tasks.input).addClass("btn-danger").css({'color':'white','font-weight': 'bold'});
	},
	create_tasks: function(frm){
		if (cur_frm.doc.__unsaved == 1) {
			frappe.throw('Save, to proceed!');
		}
		else{
			frappe.call({
				method: 'iac_activity_logger.iac_activity_logger.doctype.tasks.tasks.get_tasks',
				args:{"start":frm.doc.task_date,
						"end": frm.doc.repeat_till,
						"user": frm.doc.name
				},
				callback: function(r){
					frappe.call({
						method: 'iac_activity_logger.iac_activity_logger.doctype.tasks.tasks.del_duplicate',
						args:{"start":frm.doc.task_date
						},
						callback: function(r){
							frappe.msgprint('Recurrence Tasks Created')
							frm.reload_doc()
						}
					});
				}
			});
		}

	},
	reschedule_tasks: function(frm){
		if (cur_frm.doc.__unsaved == 1) {
			frappe.throw('Save, to proceed!');
		}
		else {
			frappe.call({
				method: 'iac_activity_logger.iac_activity_logger.doctype.tasks.tasks.delete_tasks',
				args:{"start":frm.doc.task_date,
						"end": frm.doc.repeat_till,
						"user": frm.doc.name
			},
			callback: function(r){
				frappe.msgprint('Tasks Rescheduled')
				cur_frm.reload_doc();
			}
		});
		}
	},
	repeat_on: function(frm) {
		if (frm.doc.reschedule == 1) {
			frappe.confirm('Are you sure you want to change repeat on & clear scheduled records?',
			    () => {
			        // action to perform if Yes is selected
			        frappe.call({
			        	method: 'iac_activity_logger.iac_activity_logger.doctype.tasks.tasks.delete_tasks_repeat',
						args:{"start":frm.doc.task_date,
							"end": frm.doc.repeat_till,
							"user": frm.doc.name
						},
						callback: function(r){
							frappe.msgprint('Repeat on Updated')
							frm.doc.child_tasks = "";
							cur_frm.refresh_fields();
							//cur_frm.reload_doc();
						}
					});
			    }, () => {
			        // action to perform if No is selected
			        cur_frm.reload_doc();
			    })
		}
		if(frm.doc.repeat_on != "Weekly"){
			frm.doc.monday = '';
			frm.doc.tuesday = '';
			frm.doc.wednesday = '';
			frm.doc.thursday = '';
			frm.doc.friday = '';
			frm.doc.saturday = '';
			frm.doc.sunday = '';
			cur_frm.refresh_fields();
		}
	}
});
