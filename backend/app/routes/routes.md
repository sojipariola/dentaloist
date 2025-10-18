(.venv) soji@soji-Aurora-R3:~/Documents/Projects/Dentaloist/backend$ flask list-routes-grp
Generated FERNET_KEY from SECRET_KEY
Flask-Admin initialized at /admin
✅ Template folder: templates
✅ CLI commands registered.

🔹 Blueprint: No Blueprint
------------------------
health                              GET,HEAD,OPTIONS     /health
healthz                             GET,HEAD,OPTIONS     /healthz
root                                GET,HEAD,OPTIONS     /
static                              GET,HEAD,OPTIONS     /static/<path:filename>

🔹 Blueprint: WebAuth
-------------------
WebAuth.web_login                   GET,HEAD,OPTIONS,POST /web/login
WebAuth.web_logout                  GET,HEAD,OPTIONS     /web/logout

🔹 Blueprint: admin
-----------------
admin.index                         GET,HEAD,OPTIONS     /admin/
admin.static                        GET,HEAD,OPTIONS     /admin/static/<path:filename>

🔹 Blueprint: allergy
-------------------
allergy.action_view                 OPTIONS,POST         /admin/allergy/action/
allergy.ajax_lookup                 GET,HEAD,OPTIONS     /admin/allergy/ajax/lookup/
allergy.ajax_update                 OPTIONS,POST         /admin/allergy/ajax/update/
allergy.create_view                 GET,HEAD,OPTIONS,POST /admin/allergy/new/
allergy.delete_view                 OPTIONS,POST         /admin/allergy/delete/
allergy.details_view                GET,HEAD,OPTIONS     /admin/allergy/details/
allergy.edit_view                   GET,HEAD,OPTIONS,POST /admin/allergy/edit/
allergy.export                      GET,HEAD,OPTIONS     /admin/allergy/export/<export_type>/
allergy.index_view                  GET,HEAD,OPTIONS     /admin/allergy/

🔹 Blueprint: analytics
---------------------
analytics.get_appointment_analytics GET,HEAD,OPTIONS     /api/analytics/appointments
analytics.get_dashboard_analytics   GET,HEAD,OPTIONS     /api/analytics/dashboard
analytics.get_patient_analytics     GET,HEAD,OPTIONS     /api/analytics/patients
analytics.get_revenue_analytics     GET,HEAD,OPTIONS     /api/analytics/revenue

🔹 Blueprint: api-docs
--------------------
api-docs.openapi_json               GET,HEAD,OPTIONS     /openapi.json
api-docs.openapi_swagger_ui         GET,HEAD,OPTIONS     /docs

🔹 Blueprint: appointment
-----------------------
appointment.action_view             OPTIONS,POST         /admin/appointment/action/
appointment.ajax_lookup             GET,HEAD,OPTIONS     /admin/appointment/ajax/lookup/
appointment.ajax_update             OPTIONS,POST         /admin/appointment/ajax/update/
appointment.create_view             GET,HEAD,OPTIONS,POST /admin/appointment/new/
appointment.delete_view             OPTIONS,POST         /admin/appointment/delete/
appointment.details_view            GET,HEAD,OPTIONS     /admin/appointment/details/
appointment.edit_view               GET,HEAD,OPTIONS,POST /admin/appointment/edit/
appointment.export                  GET,HEAD,OPTIONS     /admin/appointment/export/<export_type>/
appointment.index_view              GET,HEAD,OPTIONS     /admin/appointment/

🔹 Blueprint: appointments
------------------------
appointments.cancel_appointment     OPTIONS,POST         /api/appointments/<int:appointment_id>/cancel
appointments.check_availability     GET,HEAD,OPTIONS     /api/appointments/availability
appointments.complete_appointment   OPTIONS,POST         /api/appointments/<int:appointment_id>/complete
appointments.create_appointment     OPTIONS,POST         /api/appointments/
appointments.delete_appointment     DELETE,OPTIONS       /api/appointments/<int:appointment_id>
appointments.get_appointment        GET,HEAD,OPTIONS     /api/appointments/<int:appointment_id>
appointments.get_appointments       GET,HEAD,OPTIONS     /api/appointments/
appointments.get_today_appointments GET,HEAD,OPTIONS     /api/appointments/today
appointments.get_upcoming_appointments GET,HEAD,OPTIONS     /api/appointments/upcoming
appointments.update_appointment     OPTIONS,PUT          /api/appointments/<int:appointment_id>

🔹 Blueprint: audit
-----------------
audit.export_audit_logs             GET,HEAD,OPTIONS     /api/audit/logs/export
audit.get_audit_logs                GET,HEAD,OPTIONS     /api/audit/logs
audit.get_audit_statistics          GET,HEAD,OPTIONS     /api/audit/stats
audit.get_user_activity             GET,HEAD,OPTIONS     /api/audit/users/<int:user_id>/activity
audit.manage_audit_config           GET,HEAD,OPTIONS,PUT /api/audit/config

🔹 Blueprint: audittrail
----------------------
audittrail.action_view              OPTIONS,POST         /admin/audittrail/action/
audittrail.ajax_lookup              GET,HEAD,OPTIONS     /admin/audittrail/ajax/lookup/
audittrail.ajax_update              OPTIONS,POST         /admin/audittrail/ajax/update/
audittrail.create_view              GET,HEAD,OPTIONS,POST /admin/audittrail/new/
audittrail.delete_view              OPTIONS,POST         /admin/audittrail/delete/
audittrail.details_view             GET,HEAD,OPTIONS     /admin/audittrail/details/
audittrail.edit_view                GET,HEAD,OPTIONS,POST /admin/audittrail/edit/
audittrail.export                   GET,HEAD,OPTIONS     /admin/audittrail/export/<export_type>/
audittrail.index_view               GET,HEAD,OPTIONS     /admin/audittrail/

🔹 Blueprint: auth
----------------
auth.change_password                OPTIONS,POST         /api/auth/change-password
auth.forgot_password                OPTIONS,POST         /api/auth/forgot-password
auth.get_sessions                   GET,HEAD,OPTIONS     /api/auth/sessions
auth.google_callback                GET,HEAD,OPTIONS     /api/auth/google/callback
auth.google_login                   GET,HEAD,OPTIONS     /api/auth/google/login
auth.health_check                   GET,HEAD,OPTIONS     /api/auth/health
auth.login                          OPTIONS,POST         /api/auth/login
auth.login_form                     GET,HEAD,OPTIONS,POST /api/auth/login-form
auth.logout                         OPTIONS,POST         /api/auth/logout
auth.logout_all                     OPTIONS,POST         /api/auth/logout-all
auth.me                             GET,HEAD,OPTIONS     /api/auth/me
auth.refresh                        OPTIONS,POST         /api/auth/refresh
auth.register                       OPTIONS,POST         /api/auth/register
auth.reset_password                 OPTIONS,POST         /api/auth/reset-password
auth.revoke_session                 DELETE,OPTIONS       /api/auth/sessions/<int:session_id>

🔹 Blueprint: availabilityslot
----------------------------
availabilityslot.action_view        OPTIONS,POST         /admin/availabilityslot/action/
availabilityslot.ajax_lookup        GET,HEAD,OPTIONS     /admin/availabilityslot/ajax/lookup/
availabilityslot.ajax_update        OPTIONS,POST         /admin/availabilityslot/ajax/update/
availabilityslot.create_view        GET,HEAD,OPTIONS,POST /admin/availabilityslot/new/
availabilityslot.delete_view        OPTIONS,POST         /admin/availabilityslot/delete/
availabilityslot.details_view       GET,HEAD,OPTIONS     /admin/availabilityslot/details/
availabilityslot.edit_view          GET,HEAD,OPTIONS,POST /admin/availabilityslot/edit/
availabilityslot.export             GET,HEAD,OPTIONS     /admin/availabilityslot/export/<export_type>/
availabilityslot.index_view         GET,HEAD,OPTIONS     /admin/availabilityslot/

🔹 Blueprint: billing
-------------------
billing.billing_dashboard           GET,HEAD,OPTIONS     /api/billing/dashboard
billing.create_insurance_claim      OPTIONS,POST         /api/billing/insurance-claims
billing.create_invoice              OPTIONS,POST         /api/billing/invoices
billing.create_payment              OPTIONS,POST         /api/billing/payments
billing.delete_invoice              DELETE,OPTIONS       /api/billing/invoices/<int:invoice_id>
billing.delete_payment              DELETE,OPTIONS       /api/billing/payments/<int:payment_id>
billing.get_invoice                 GET,HEAD,OPTIONS     /api/billing/invoices/<int:invoice_id>
billing.get_invoices                GET,HEAD,OPTIONS     /api/billing/invoices
billing.update_insurance_claim      OPTIONS,PUT          /api/billing/insurance-claims/<int:claim_id>
billing.update_invoice              OPTIONS,PUT          /api/billing/invoices/<int:invoice_id>

🔹 Blueprint: clinical
--------------------
clinical.create_medical_record      OPTIONS,POST         /api/clinical/records
clinical.delete_medical_attachment  DELETE,OPTIONS       /api/clinical/records/<int:record_id>/attachments/<attachment_id>
clinical.delete_medical_record      DELETE,OPTIONS       /api/clinical/records/<int:record_id>
clinical.get_medical_record         GET,HEAD,OPTIONS     /api/clinical/records/<int:record_id>
clinical.get_medical_records        GET,HEAD,OPTIONS     /api/clinical/records
clinical.lock_medical_record        OPTIONS,POST         /api/clinical/records/<int:record_id>/lock
clinical.patient_clinical_dashboard GET,HEAD,OPTIONS     /api/clinical/dashboard/patient/<int:patient_id>
clinical.search_clinical_data       GET,HEAD,OPTIONS     /api/clinical/search
clinical.update_medical_record      OPTIONS,PUT          /api/clinical/records/<int:record_id>
clinical.upload_medical_attachment  OPTIONS,POST         /api/clinical/records/<int:record_id>/attachments

🔹 Blueprint: dashboard
---------------------
dashboard.create_widget             OPTIONS,POST         /api/dashboard/widgets
dashboard.delete_widget             DELETE,OPTIONS       /api/dashboard/widgets/<int:widget_id>
dashboard.get_appointment_stats     GET,HEAD,OPTIONS     /api/dashboard/data/appointment-stats
dashboard.get_dashboard_layout      GET,HEAD,OPTIONS     /api/dashboard/layout
dashboard.get_financial_overview    GET,HEAD,OPTIONS     /api/dashboard/data/financial-overview
dashboard.get_patient_metrics       GET,HEAD,OPTIONS     /api/dashboard/data/patient-metrics
dashboard.get_widget_data           GET,HEAD,OPTIONS     /api/dashboard/data/widget/<widget_type>
dashboard.get_widgets               GET,HEAD,OPTIONS     /api/dashboard/widgets
dashboard.reset_widgets             OPTIONS,POST         /api/dashboard/widgets/reset
dashboard.update_dashboard_layout   OPTIONS,PUT          /api/dashboard/layout
dashboard.update_widget             OPTIONS,PUT          /api/dashboard/widgets/<int:widget_id>

🔹 Blueprint: diagnosis
---------------------
diagnosis.action_view               OPTIONS,POST         /admin/diagnosis/action/
diagnosis.ajax_lookup               GET,HEAD,OPTIONS     /admin/diagnosis/ajax/lookup/
diagnosis.ajax_update               OPTIONS,POST         /admin/diagnosis/ajax/update/
diagnosis.create_view               GET,HEAD,OPTIONS,POST /admin/diagnosis/new/
diagnosis.delete_view               OPTIONS,POST         /admin/diagnosis/delete/
diagnosis.details_view              GET,HEAD,OPTIONS     /admin/diagnosis/details/
diagnosis.edit_view                 GET,HEAD,OPTIONS,POST /admin/diagnosis/edit/
diagnosis.export                    GET,HEAD,OPTIONS     /admin/diagnosis/export/<export_type>/
diagnosis.index_view                GET,HEAD,OPTIONS     /admin/diagnosis/

🔹 Blueprint: expense
-------------------
expense.action_view                 OPTIONS,POST         /admin/expense/action/
expense.ajax_lookup                 GET,HEAD,OPTIONS     /admin/expense/ajax/lookup/
expense.ajax_update                 OPTIONS,POST         /admin/expense/ajax/update/
expense.create_view                 GET,HEAD,OPTIONS,POST /admin/expense/new/
expense.delete_view                 OPTIONS,POST         /admin/expense/delete/
expense.details_view                GET,HEAD,OPTIONS     /admin/expense/details/
expense.edit_view                   GET,HEAD,OPTIONS,POST /admin/expense/edit/
expense.export                      GET,HEAD,OPTIONS     /admin/expense/export/<export_type>/
expense.index_view                  GET,HEAD,OPTIONS     /admin/expense/

🔹 Blueprint: family_members
--------------------------
family_members.create_family_member OPTIONS,POST         /api/family_members
family_members.create_family_relationship OPTIONS,POST         /api/family_members/<int:fm_id>/relationships
family_members.delete_family_member DELETE,OPTIONS       /api/family_members/<int:fm_id>
family_members.delete_family_relationship DELETE,OPTIONS       /api/family_members/relationships/<int:relationship_id>
family_members.get_family_member    GET,HEAD,OPTIONS     /api/family_members/<int:fm_id>
family_members.get_family_member_insurance GET,HEAD,OPTIONS     /api/family_members/<int:fm_id>/insurance
family_members.get_family_relationships GET,HEAD,OPTIONS     /api/family_members/<int:fm_id>/relationships
family_members.list_family_members  GET,HEAD,OPTIONS     /api/family_members
family_members.update_family_member OPTIONS,PUT          /api/family_members/<int:fm_id>

🔹 Blueprint: familymember
------------------------
familymember.action_view            OPTIONS,POST         /admin/familymember/action/
familymember.ajax_lookup            GET,HEAD,OPTIONS     /admin/familymember/ajax/lookup/
familymember.ajax_update            OPTIONS,POST         /admin/familymember/ajax/update/
familymember.create_view            GET,HEAD,OPTIONS,POST /admin/familymember/new/
familymember.delete_view            OPTIONS,POST         /admin/familymember/delete/
familymember.details_view           GET,HEAD,OPTIONS     /admin/familymember/details/
familymember.edit_view              GET,HEAD,OPTIONS,POST /admin/familymember/edit/
familymember.export                 GET,HEAD,OPTIONS     /admin/familymember/export/<export_type>/
familymember.index_view             GET,HEAD,OPTIONS     /admin/familymember/

🔹 Blueprint: familyrelationship
------------------------------
familyrelationship.action_view      OPTIONS,POST         /admin/familyrelationship/action/
familyrelationship.ajax_lookup      GET,HEAD,OPTIONS     /admin/familyrelationship/ajax/lookup/
familyrelationship.ajax_update      OPTIONS,POST         /admin/familyrelationship/ajax/update/
familyrelationship.create_view      GET,HEAD,OPTIONS,POST /admin/familyrelationship/new/
familyrelationship.delete_view      OPTIONS,POST         /admin/familyrelationship/delete/
familyrelationship.details_view     GET,HEAD,OPTIONS     /admin/familyrelationship/details/
familyrelationship.edit_view        GET,HEAD,OPTIONS,POST /admin/familyrelationship/edit/
familyrelationship.export           GET,HEAD,OPTIONS     /admin/familyrelationship/export/<export_type>/
familyrelationship.index_view       GET,HEAD,OPTIONS     /admin/familyrelationship/

🔹 Blueprint: filerecord
----------------------
filerecord.action_view              OPTIONS,POST         /admin/filerecord/action/
filerecord.ajax_lookup              GET,HEAD,OPTIONS     /admin/filerecord/ajax/lookup/
filerecord.ajax_update              OPTIONS,POST         /admin/filerecord/ajax/update/
filerecord.create_view              GET,HEAD,OPTIONS,POST /admin/filerecord/new/
filerecord.delete_view              OPTIONS,POST         /admin/filerecord/delete/
filerecord.details_view             GET,HEAD,OPTIONS     /admin/filerecord/details/
filerecord.edit_view                GET,HEAD,OPTIONS,POST /admin/filerecord/edit/
filerecord.export                   GET,HEAD,OPTIONS     /admin/filerecord/export/<export_type>/
filerecord.index_view               GET,HEAD,OPTIONS     /admin/filerecord/

🔹 Blueprint: files
-----------------
files.get_files                     GET,HEAD,OPTIONS     /api/files/
files.upload_file                   OPTIONS,POST         /api/files/upload

🔹 Blueprint: health
------------------
health.detailed_health              GET,HEAD,OPTIONS     /api/health/detailed
health.health_check                 GET,HEAD,OPTIONS     /api/health/
health.liveness_probe               GET,HEAD,OPTIONS     /api/health/liveness
health.metrics                      GET,HEAD,OPTIONS     /api/health/metrics
health.readiness_probe              GET,HEAD,OPTIONS     /api/health/readiness
health.status                       GET,HEAD,OPTIONS     /api/health/status

🔹 Blueprint: immunization
------------------------
immunization.action_view            OPTIONS,POST         /admin/immunization/action/
immunization.ajax_lookup            GET,HEAD,OPTIONS     /admin/immunization/ajax/lookup/
immunization.ajax_update            OPTIONS,POST         /admin/immunization/ajax/update/
immunization.create_view            GET,HEAD,OPTIONS,POST /admin/immunization/new/
immunization.delete_view            OPTIONS,POST         /admin/immunization/delete/
immunization.details_view           GET,HEAD,OPTIONS     /admin/immunization/details/
immunization.edit_view              GET,HEAD,OPTIONS,POST /admin/immunization/edit/
immunization.export                 GET,HEAD,OPTIONS     /admin/immunization/export/<export_type>/
immunization.index_view             GET,HEAD,OPTIONS     /admin/immunization/

🔹 Blueprint: insurance
---------------------
insurance.check_insurance_coverage  OPTIONS,POST         /api/insurance/coverage/check
insurance.create_insurance_plan     OPTIONS,POST         /api/insurance/plans
insurance.delete_insurance_plan     DELETE,OPTIONS       /api/insurance/plans/<int:plan_id>
insurance.get_insurance_coverage    GET,HEAD,OPTIONS     /api/insurance/plans/<int:plan_id>/coverage
insurance.get_insurance_plan        GET,HEAD,OPTIONS     /api/insurance/plans/<int:plan_id>
insurance.list_insurance_plans      GET,HEAD,OPTIONS     /api/insurance/plans
insurance.update_insurance_plan     OPTIONS,PUT          /api/insurance/plans/<int:plan_id>
insurance.verify_insurance_plan     OPTIONS,POST         /api/insurance/plans/<int:plan_id>/verify

🔹 Blueprint: insuranceclaim
--------------------------
insuranceclaim.action_view          OPTIONS,POST         /admin/insuranceclaim/action/
insuranceclaim.ajax_lookup          GET,HEAD,OPTIONS     /admin/insuranceclaim/ajax/lookup/
insuranceclaim.ajax_update          OPTIONS,POST         /admin/insuranceclaim/ajax/update/
insuranceclaim.create_view          GET,HEAD,OPTIONS,POST /admin/insuranceclaim/new/
insuranceclaim.delete_view          OPTIONS,POST         /admin/insuranceclaim/delete/
insuranceclaim.details_view         GET,HEAD,OPTIONS     /admin/insuranceclaim/details/
insuranceclaim.edit_view            GET,HEAD,OPTIONS,POST /admin/insuranceclaim/edit/
insuranceclaim.export               GET,HEAD,OPTIONS     /admin/insuranceclaim/export/<export_type>/
insuranceclaim.index_view           GET,HEAD,OPTIONS     /admin/insuranceclaim/

🔹 Blueprint: insuranceplan
-------------------------
insuranceplan.action_view           OPTIONS,POST         /admin/insuranceplan/action/
insuranceplan.ajax_lookup           GET,HEAD,OPTIONS     /admin/insuranceplan/ajax/lookup/
insuranceplan.ajax_update           OPTIONS,POST         /admin/insuranceplan/ajax/update/
insuranceplan.create_view           GET,HEAD,OPTIONS,POST /admin/insuranceplan/new/
insuranceplan.delete_view           OPTIONS,POST         /admin/insuranceplan/delete/
insuranceplan.details_view          GET,HEAD,OPTIONS     /admin/insuranceplan/details/
insuranceplan.edit_view             GET,HEAD,OPTIONS,POST /admin/insuranceplan/edit/
insuranceplan.export                GET,HEAD,OPTIONS     /admin/insuranceplan/export/<export_type>/
insuranceplan.index_view            GET,HEAD,OPTIONS     /admin/insuranceplan/

🔹 Blueprint: integration
-----------------------
integration.action_view             OPTIONS,POST         /admin/integration/action/
integration.ajax_lookup             GET,HEAD,OPTIONS     /admin/integration/ajax/lookup/
integration.ajax_update             OPTIONS,POST         /admin/integration/ajax/update/
integration.create_view             GET,HEAD,OPTIONS,POST /admin/integration/new/
integration.delete_view             OPTIONS,POST         /admin/integration/delete/
integration.details_view            GET,HEAD,OPTIONS     /admin/integration/details/
integration.edit_view               GET,HEAD,OPTIONS,POST /admin/integration/edit/
integration.export                  GET,HEAD,OPTIONS     /admin/integration/export/<export_type>/
integration.index_view              GET,HEAD,OPTIONS     /admin/integration/

🔹 Blueprint: integrationlog
--------------------------
integrationlog.action_view          OPTIONS,POST         /admin/integrationlog/action/
integrationlog.ajax_lookup          GET,HEAD,OPTIONS     /admin/integrationlog/ajax/lookup/
integrationlog.ajax_update          OPTIONS,POST         /admin/integrationlog/ajax/update/
integrationlog.create_view          GET,HEAD,OPTIONS,POST /admin/integrationlog/new/
integrationlog.delete_view          OPTIONS,POST         /admin/integrationlog/delete/
integrationlog.details_view         GET,HEAD,OPTIONS     /admin/integrationlog/details/
integrationlog.edit_view            GET,HEAD,OPTIONS,POST /admin/integrationlog/edit/
integrationlog.export               GET,HEAD,OPTIONS     /admin/integrationlog/export/<export_type>/
integrationlog.index_view           GET,HEAD,OPTIONS     /admin/integrationlog/

🔹 Blueprint: integrations
------------------------
integrations.create_update_integration OPTIONS,POST         /api/integrations/<integration_type>
integrations.create_webhook         OPTIONS,POST         /api/integrations/<integration_type>/webhooks
integrations.delete_integration     DELETE,OPTIONS       /api/integrations/<integration_type>
integrations.get_integration_detail GET,HEAD,OPTIONS     /api/integrations/<integration_type>
integrations.get_integration_webhooks GET,HEAD,OPTIONS     /api/integrations/<integration_type>/webhooks
integrations.get_integrations       GET,HEAD,OPTIONS     /api/integrations/
integrations.init_oauth_integration GET,HEAD,OPTIONS     /api/integrations/<integration_type>/oauth/init
integrations.oauth_callback         GET,HEAD,OPTIONS     /api/integrations/<integration_type>/oauth/callback
integrations.test_integration       OPTIONS,POST         /api/integrations/<integration_type>/test
integrations.trigger_sync           OPTIONS,POST         /api/integrations/<integration_type>/sync

🔹 Blueprint: inventory
---------------------
inventory.create_inventory_item     OPTIONS,POST         /api/inventory/items
inventory.create_inventory_transaction OPTIONS,POST         /api/inventory/transactions
inventory.delete_inventory_item     DELETE,OPTIONS       /api/inventory/items/<int:item_id>
inventory.get_inventory_item        GET,HEAD,OPTIONS     /api/inventory/items/<int:item_id>
inventory.get_inventory_items       GET,HEAD,OPTIONS     /api/inventory/items
inventory.get_inventory_summary     GET,HEAD,OPTIONS     /api/inventory/reports/summary
inventory.get_inventory_transactions GET,HEAD,OPTIONS     /api/inventory/transactions
inventory.get_inventory_valuation   GET,HEAD,OPTIONS     /api/inventory/reports/valuation
inventory.update_inventory_item     OPTIONS,PUT          /api/inventory/items/<int:item_id>

🔹 Blueprint: inventoryadjustment
-------------------------------
inventoryadjustment.action_view     OPTIONS,POST         /admin/inventoryadjustment/action/
inventoryadjustment.ajax_lookup     GET,HEAD,OPTIONS     /admin/inventoryadjustment/ajax/lookup/
inventoryadjustment.ajax_update     OPTIONS,POST         /admin/inventoryadjustment/ajax/update/
inventoryadjustment.create_view     GET,HEAD,OPTIONS,POST /admin/inventoryadjustment/new/
inventoryadjustment.delete_view     OPTIONS,POST         /admin/inventoryadjustment/delete/
inventoryadjustment.details_view    GET,HEAD,OPTIONS     /admin/inventoryadjustment/details/
inventoryadjustment.edit_view       GET,HEAD,OPTIONS,POST /admin/inventoryadjustment/edit/
inventoryadjustment.export          GET,HEAD,OPTIONS     /admin/inventoryadjustment/export/<export_type>/
inventoryadjustment.index_view      GET,HEAD,OPTIONS     /admin/inventoryadjustment/

🔹 Blueprint: inventoryitem
-------------------------
inventoryitem.action_view           OPTIONS,POST         /admin/inventoryitem/action/
inventoryitem.ajax_lookup           GET,HEAD,OPTIONS     /admin/inventoryitem/ajax/lookup/
inventoryitem.ajax_update           OPTIONS,POST         /admin/inventoryitem/ajax/update/
inventoryitem.create_view           GET,HEAD,OPTIONS,POST /admin/inventoryitem/new/
inventoryitem.delete_view           OPTIONS,POST         /admin/inventoryitem/delete/
inventoryitem.details_view          GET,HEAD,OPTIONS     /admin/inventoryitem/details/
inventoryitem.edit_view             GET,HEAD,OPTIONS,POST /admin/inventoryitem/edit/
inventoryitem.export                GET,HEAD,OPTIONS     /admin/inventoryitem/export/<export_type>/
inventoryitem.index_view            GET,HEAD,OPTIONS     /admin/inventoryitem/

🔹 Blueprint: inventorytransaction
--------------------------------
inventorytransaction.action_view    OPTIONS,POST         /admin/inventorytransaction/action/
inventorytransaction.ajax_lookup    GET,HEAD,OPTIONS     /admin/inventorytransaction/ajax/lookup/
inventorytransaction.ajax_update    OPTIONS,POST         /admin/inventorytransaction/ajax/update/
inventorytransaction.create_view    GET,HEAD,OPTIONS,POST /admin/inventorytransaction/new/
inventorytransaction.delete_view    OPTIONS,POST         /admin/inventorytransaction/delete/
inventorytransaction.details_view   GET,HEAD,OPTIONS     /admin/inventorytransaction/details/
inventorytransaction.edit_view      GET,HEAD,OPTIONS,POST /admin/inventorytransaction/edit/
inventorytransaction.export         GET,HEAD,OPTIONS     /admin/inventorytransaction/export/<export_type>/
inventorytransaction.index_view     GET,HEAD,OPTIONS     /admin/inventorytransaction/

🔹 Blueprint: invoice
-------------------
invoice.action_view                 OPTIONS,POST         /admin/invoice/action/
invoice.ajax_lookup                 GET,HEAD,OPTIONS     /admin/invoice/ajax/lookup/
invoice.ajax_update                 OPTIONS,POST         /admin/invoice/ajax/update/
invoice.create_view                 GET,HEAD,OPTIONS,POST /admin/invoice/new/
invoice.delete_view                 OPTIONS,POST         /admin/invoice/delete/
invoice.details_view                GET,HEAD,OPTIONS     /admin/invoice/details/
invoice.edit_view                   GET,HEAD,OPTIONS,POST /admin/invoice/edit/
invoice.export                      GET,HEAD,OPTIONS     /admin/invoice/export/<export_type>/
invoice.index_view                  GET,HEAD,OPTIONS     /admin/invoice/

🔹 Blueprint: laborder
--------------------
laborder.action_view                OPTIONS,POST         /admin/laborder/action/
laborder.ajax_lookup                GET,HEAD,OPTIONS     /admin/laborder/ajax/lookup/
laborder.ajax_update                OPTIONS,POST         /admin/laborder/ajax/update/
laborder.create_view                GET,HEAD,OPTIONS,POST /admin/laborder/new/
laborder.delete_view                OPTIONS,POST         /admin/laborder/delete/
laborder.details_view               GET,HEAD,OPTIONS     /admin/laborder/details/
laborder.edit_view                  GET,HEAD,OPTIONS,POST /admin/laborder/edit/
laborder.export                     GET,HEAD,OPTIONS     /admin/laborder/export/<export_type>/
laborder.index_view                 GET,HEAD,OPTIONS     /admin/laborder/

🔹 Blueprint: labs
----------------
labs.add_lab_results                OPTIONS,POST         /api/labs/orders/<int:order_id>/results
labs.approve_lab_results            OPTIONS,POST         /api/labs/orders/<int:order_id>/approve
labs.create_lab_order               OPTIONS,POST         /api/labs/orders
labs.get_lab_order                  GET,HEAD,OPTIONS     /api/labs/orders/<int:order_id>
labs.get_lab_orders                 GET,HEAD,OPTIONS     /api/labs/orders
labs.get_lab_stats                  GET,HEAD,OPTIONS     /api/labs/stats
labs.reject_lab_results             OPTIONS,POST         /api/labs/orders/<int:order_id>/reject
labs.update_lab_order               OPTIONS,PUT          /api/labs/orders/<int:order_id>
labs.update_lab_order_status        OPTIONS,PUT          /api/labs/orders/<int:order_id>/status

🔹 Blueprint: medicalrecord
-------------------------
medicalrecord.action_view           OPTIONS,POST         /admin/medicalrecord/action/
medicalrecord.ajax_lookup           GET,HEAD,OPTIONS     /admin/medicalrecord/ajax/lookup/
medicalrecord.ajax_update           OPTIONS,POST         /admin/medicalrecord/ajax/update/
medicalrecord.create_view           GET,HEAD,OPTIONS,POST /admin/medicalrecord/new/
medicalrecord.delete_view           OPTIONS,POST         /admin/medicalrecord/delete/
medicalrecord.details_view          GET,HEAD,OPTIONS     /admin/medicalrecord/details/
medicalrecord.edit_view             GET,HEAD,OPTIONS,POST /admin/medicalrecord/edit/
medicalrecord.export                GET,HEAD,OPTIONS     /admin/medicalrecord/export/<export_type>/
medicalrecord.index_view            GET,HEAD,OPTIONS     /admin/medicalrecord/

🔹 Blueprint: medication
----------------------
medication.action_view              OPTIONS,POST         /admin/medication/action/
medication.ajax_lookup              GET,HEAD,OPTIONS     /admin/medication/ajax/lookup/
medication.ajax_update              OPTIONS,POST         /admin/medication/ajax/update/
medication.create_view              GET,HEAD,OPTIONS,POST /admin/medication/new/
medication.delete_view              OPTIONS,POST         /admin/medication/delete/
medication.details_view             GET,HEAD,OPTIONS     /admin/medication/details/
medication.edit_view                GET,HEAD,OPTIONS,POST /admin/medication/edit/
medication.export                   GET,HEAD,OPTIONS     /admin/medication/export/<export_type>/
medication.index_view               GET,HEAD,OPTIONS     /admin/medication/

🔹 Blueprint: note
----------------
note.action_view                    OPTIONS,POST         /admin/note/action/
note.ajax_lookup                    GET,HEAD,OPTIONS     /admin/note/ajax/lookup/
note.ajax_update                    OPTIONS,POST         /admin/note/ajax/update/
note.create_view                    GET,HEAD,OPTIONS,POST /admin/note/new/
note.delete_view                    OPTIONS,POST         /admin/note/delete/
note.details_view                   GET,HEAD,OPTIONS     /admin/note/details/
note.edit_view                      GET,HEAD,OPTIONS,POST /admin/note/edit/
note.export                         GET,HEAD,OPTIONS     /admin/note/export/<export_type>/
note.index_view                     GET,HEAD,OPTIONS     /admin/note/

🔹 Blueprint: notification
------------------------
notification.action_view            OPTIONS,POST         /admin/notification/action/
notification.ajax_lookup            GET,HEAD,OPTIONS     /admin/notification/ajax/lookup/
notification.ajax_update            OPTIONS,POST         /admin/notification/ajax/update/
notification.create_view            GET,HEAD,OPTIONS,POST /admin/notification/new/
notification.delete_view            OPTIONS,POST         /admin/notification/delete/
notification.details_view           GET,HEAD,OPTIONS     /admin/notification/details/
notification.edit_view              GET,HEAD,OPTIONS,POST /admin/notification/edit/
notification.export                 GET,HEAD,OPTIONS     /admin/notification/export/<export_type>/
notification.index_view             GET,HEAD,OPTIONS     /admin/notification/

🔹 Blueprint: notifications
-------------------------
notifications.bulk_notification_actions OPTIONS,POST         /api/notifications/bulk-action
notifications.clear_all_notifications OPTIONS,POST         /api/notifications/clear-all
notifications.get_notification      GET,HEAD,OPTIONS     /api/notifications/<int:notification_id>
notifications.get_notification_statistics GET,HEAD,OPTIONS     /api/notifications/stats
notifications.get_notifications     GET,HEAD,OPTIONS     /api/notifications/
notifications.manage_notification_preferences GET,HEAD,OPTIONS,PUT /api/notifications/preferences
notifications.mark_all_as_read      OPTIONS,POST         /api/notifications/read-all
notifications.mark_as_read          OPTIONS,POST         /api/notifications/<int:notification_id>/read
notifications.mark_as_unread        OPTIONS,POST         /api/notifications/<int:notification_id>/unread
notifications.send_notification     OPTIONS,POST         /api/notifications/send

🔹 Blueprint: organization
------------------------
organization.action_view            OPTIONS,POST         /admin/organization/action/
organization.ajax_lookup            GET,HEAD,OPTIONS     /admin/organization/ajax/lookup/
organization.ajax_update            OPTIONS,POST         /admin/organization/ajax/update/
organization.create_view            GET,HEAD,OPTIONS,POST /admin/organization/new/
organization.delete_view            OPTIONS,POST         /admin/organization/delete/
organization.details_view           GET,HEAD,OPTIONS     /admin/organization/details/
organization.edit_view              GET,HEAD,OPTIONS,POST /admin/organization/edit/
organization.export                 GET,HEAD,OPTIONS     /admin/organization/export/<export_type>/
organization.index_view             GET,HEAD,OPTIONS     /admin/organization/

🔹 Blueprint: organizations
-------------------------
organizations.create_organization   OPTIONS,POST         /api/organizations/
organizations.delete_organization   DELETE,OPTIONS       /api/organizations/<org_id>
organizations.get_current_organization GET,HEAD,OPTIONS     /api/organizations/current
organizations.get_organization      GET,HEAD,OPTIONS     /api/organizations/<org_id>
organizations.get_organization_stats GET,HEAD,OPTIONS     /api/organizations/<org_id>/stats
organizations.get_organization_users GET,HEAD,OPTIONS     /api/organizations/<org_id>/users
organizations.get_organizations     GET,HEAD,OPTIONS     /api/organizations/
organizations.manage_organization_settings GET,HEAD,OPTIONS,PUT /api/organizations/<org_id>/settings
organizations.update_organization   OPTIONS,PUT          /api/organizations/<org_id>
organizations.update_subscription   OPTIONS,PUT          /api/organizations/<org_id>/subscription

🔹 Blueprint: patient
-------------------
patient.action_view                 OPTIONS,POST         /admin/patient/action/
patient.ajax_lookup                 GET,HEAD,OPTIONS     /admin/patient/ajax/lookup/
patient.ajax_update                 OPTIONS,POST         /admin/patient/ajax/update/
patient.create_view                 GET,HEAD,OPTIONS,POST /admin/patient/new/
patient.delete_view                 OPTIONS,POST         /admin/patient/delete/
patient.details_view                GET,HEAD,OPTIONS     /admin/patient/details/
patient.edit_view                   GET,HEAD,OPTIONS,POST /admin/patient/edit/
patient.export                      GET,HEAD,OPTIONS     /admin/patient/export/<export_type>/
patient.index_view                  GET,HEAD,OPTIONS     /admin/patient/

🔹 Blueprint: patients
--------------------
patients.create_patient             OPTIONS,POST         /api/patients/
patients.delete_patient             DELETE,OPTIONS       /api/patients/<int:patient_id>
patients.get_patient                GET,HEAD,OPTIONS     /api/patients/<int:patient_id>
patients.get_patient_statistics     GET,HEAD,OPTIONS     /api/patients/stats
patients.get_patients               GET,HEAD,OPTIONS     /api/patients/
patients.import_patients            OPTIONS,POST         /api/patients/import
patients.manage_medical_history     GET,HEAD,OPTIONS,POST,PUT /api/patients/<int:patient_id>/medical-history
patients.reactivate_patient         OPTIONS,POST         /api/patients/<int:patient_id>/reactivate
patients.update_patient             OPTIONS,PUT          /api/patients/<int:patient_id>

🔹 Blueprint: payment
-------------------
payment.action_view                 OPTIONS,POST         /admin/payment/action/
payment.ajax_lookup                 GET,HEAD,OPTIONS     /admin/payment/ajax/lookup/
payment.ajax_update                 OPTIONS,POST         /admin/payment/ajax/update/
payment.create_view                 GET,HEAD,OPTIONS,POST /admin/payment/new/
payment.delete_view                 OPTIONS,POST         /admin/payment/delete/
payment.details_view                GET,HEAD,OPTIONS     /admin/payment/details/
payment.edit_view                   GET,HEAD,OPTIONS,POST /admin/payment/edit/
payment.export                      GET,HEAD,OPTIONS     /admin/payment/export/<export_type>/
payment.index_view                  GET,HEAD,OPTIONS     /admin/payment/

🔹 Blueprint: paymentrecord
-------------------------
paymentrecord.action_view           OPTIONS,POST         /admin/paymentrecord/action/
paymentrecord.ajax_lookup           GET,HEAD,OPTIONS     /admin/paymentrecord/ajax/lookup/
paymentrecord.ajax_update           OPTIONS,POST         /admin/paymentrecord/ajax/update/
paymentrecord.create_view           GET,HEAD,OPTIONS,POST /admin/paymentrecord/new/
paymentrecord.delete_view           OPTIONS,POST         /admin/paymentrecord/delete/
paymentrecord.details_view          GET,HEAD,OPTIONS     /admin/paymentrecord/details/
paymentrecord.edit_view             GET,HEAD,OPTIONS,POST /admin/paymentrecord/edit/
paymentrecord.export                GET,HEAD,OPTIONS     /admin/paymentrecord/export/<export_type>/
paymentrecord.index_view            GET,HEAD,OPTIONS     /admin/paymentrecord/

🔹 Blueprint: prescription
------------------------
prescription.action_view            OPTIONS,POST         /admin/prescription/action/
prescription.ajax_lookup            GET,HEAD,OPTIONS     /admin/prescription/ajax/lookup/
prescription.ajax_update            OPTIONS,POST         /admin/prescription/ajax/update/
prescription.create_view            GET,HEAD,OPTIONS,POST /admin/prescription/new/
prescription.delete_view            OPTIONS,POST         /admin/prescription/delete/
prescription.details_view           GET,HEAD,OPTIONS     /admin/prescription/details/
prescription.edit_view              GET,HEAD,OPTIONS,POST /admin/prescription/edit/
prescription.export                 GET,HEAD,OPTIONS     /admin/prescription/export/<export_type>/
prescription.index_view             GET,HEAD,OPTIONS     /admin/prescription/

🔹 Blueprint: prescriptions
-------------------------
prescriptions.approve_prescription  OPTIONS,POST         /api/prescriptions/<int:prescription_id>/approve
prescriptions.cancel_prescription   OPTIONS,POST         /api/prescriptions/<int:prescription_id>/cancel
prescriptions.create_prescription   OPTIONS,POST         /api/prescriptions/
prescriptions.delete_prescription   DELETE,OPTIONS       /api/prescriptions/<int:prescription_id>
prescriptions.dispense_prescription OPTIONS,POST         /api/prescriptions/<int:prescription_id>/dispense
prescriptions.get_patient_prescriptions GET,HEAD,OPTIONS     /api/prescriptions/patient/<int:patient_id>
prescriptions.get_prescription      GET,HEAD,OPTIONS     /api/prescriptions/<int:prescription_id>
prescriptions.get_prescription_statistics GET,HEAD,OPTIONS     /api/prescriptions/stats
prescriptions.get_prescriptions     GET,HEAD,OPTIONS     /api/prescriptions/
prescriptions.update_prescription   OPTIONS,PUT          /api/prescriptions/<int:prescription_id>

🔹 Blueprint: product
-------------------
product.action_view                 OPTIONS,POST         /admin/product/action/
product.ajax_lookup                 GET,HEAD,OPTIONS     /admin/product/ajax/lookup/
product.ajax_update                 OPTIONS,POST         /admin/product/ajax/update/
product.create_view                 GET,HEAD,OPTIONS,POST /admin/product/new/
product.delete_view                 OPTIONS,POST         /admin/product/delete/
product.details_view                GET,HEAD,OPTIONS     /admin/product/details/
product.edit_view                   GET,HEAD,OPTIONS,POST /admin/product/edit/
product.export                      GET,HEAD,OPTIONS     /admin/product/export/<export_type>/
product.index_view                  GET,HEAD,OPTIONS     /admin/product/

🔹 Blueprint: productcategory
---------------------------
productcategory.action_view         OPTIONS,POST         /admin/productcategory/action/
productcategory.ajax_lookup         GET,HEAD,OPTIONS     /admin/productcategory/ajax/lookup/
productcategory.ajax_update         OPTIONS,POST         /admin/productcategory/ajax/update/
productcategory.create_view         GET,HEAD,OPTIONS,POST /admin/productcategory/new/
productcategory.delete_view         OPTIONS,POST         /admin/productcategory/delete/
productcategory.details_view        GET,HEAD,OPTIONS     /admin/productcategory/details/
productcategory.edit_view           GET,HEAD,OPTIONS,POST /admin/productcategory/edit/
productcategory.export              GET,HEAD,OPTIONS     /admin/productcategory/export/<export_type>/
productcategory.index_view          GET,HEAD,OPTIONS     /admin/productcategory/

🔹 Blueprint: productimage
------------------------
productimage.action_view            OPTIONS,POST         /admin/productimage/action/
productimage.ajax_lookup            GET,HEAD,OPTIONS     /admin/productimage/ajax/lookup/
productimage.ajax_update            OPTIONS,POST         /admin/productimage/ajax/update/
productimage.create_view            GET,HEAD,OPTIONS,POST /admin/productimage/new/
productimage.delete_view            OPTIONS,POST         /admin/productimage/delete/
productimage.details_view           GET,HEAD,OPTIONS     /admin/productimage/details/
productimage.edit_view              GET,HEAD,OPTIONS,POST /admin/productimage/edit/
productimage.export                 GET,HEAD,OPTIONS     /admin/productimage/export/<export_type>/
productimage.index_view             GET,HEAD,OPTIONS     /admin/productimage/

🔹 Blueprint: productpricehistory
-------------------------------
productpricehistory.action_view     OPTIONS,POST         /admin/productpricehistory/action/
productpricehistory.ajax_lookup     GET,HEAD,OPTIONS     /admin/productpricehistory/ajax/lookup/
productpricehistory.ajax_update     OPTIONS,POST         /admin/productpricehistory/ajax/update/
productpricehistory.create_view     GET,HEAD,OPTIONS,POST /admin/productpricehistory/new/
productpricehistory.delete_view     OPTIONS,POST         /admin/productpricehistory/delete/
productpricehistory.details_view    GET,HEAD,OPTIONS     /admin/productpricehistory/details/
productpricehistory.edit_view       GET,HEAD,OPTIONS,POST /admin/productpricehistory/edit/
productpricehistory.export          GET,HEAD,OPTIONS     /admin/productpricehistory/export/<export_type>/
productpricehistory.index_view      GET,HEAD,OPTIONS     /admin/productpricehistory/

🔹 Blueprint: purchaseorder
-------------------------
purchaseorder.action_view           OPTIONS,POST         /admin/purchaseorder/action/
purchaseorder.ajax_lookup           GET,HEAD,OPTIONS     /admin/purchaseorder/ajax/lookup/
purchaseorder.ajax_update           OPTIONS,POST         /admin/purchaseorder/ajax/update/
purchaseorder.create_view           GET,HEAD,OPTIONS,POST /admin/purchaseorder/new/
purchaseorder.delete_view           OPTIONS,POST         /admin/purchaseorder/delete/
purchaseorder.details_view          GET,HEAD,OPTIONS     /admin/purchaseorder/details/
purchaseorder.edit_view             GET,HEAD,OPTIONS,POST /admin/purchaseorder/edit/
purchaseorder.export                GET,HEAD,OPTIONS     /admin/purchaseorder/export/<export_type>/
purchaseorder.index_view            GET,HEAD,OPTIONS     /admin/purchaseorder/

🔹 Blueprint: purchaseorderitem
-----------------------------
purchaseorderitem.action_view       OPTIONS,POST         /admin/purchaseorderitem/action/
purchaseorderitem.ajax_lookup       GET,HEAD,OPTIONS     /admin/purchaseorderitem/ajax/lookup/
purchaseorderitem.ajax_update       OPTIONS,POST         /admin/purchaseorderitem/ajax/update/
purchaseorderitem.create_view       GET,HEAD,OPTIONS,POST /admin/purchaseorderitem/new/
purchaseorderitem.delete_view       OPTIONS,POST         /admin/purchaseorderitem/delete/
purchaseorderitem.details_view      GET,HEAD,OPTIONS     /admin/purchaseorderitem/details/
purchaseorderitem.edit_view         GET,HEAD,OPTIONS,POST /admin/purchaseorderitem/edit/
purchaseorderitem.export            GET,HEAD,OPTIONS     /admin/purchaseorderitem/export/<export_type>/
purchaseorderitem.index_view        GET,HEAD,OPTIONS     /admin/purchaseorderitem/

🔹 Blueprint: ratelimit
---------------------
ratelimit.action_view               OPTIONS,POST         /admin/ratelimit/action/
ratelimit.ajax_lookup               GET,HEAD,OPTIONS     /admin/ratelimit/ajax/lookup/
ratelimit.ajax_update               OPTIONS,POST         /admin/ratelimit/ajax/update/
ratelimit.create_view               GET,HEAD,OPTIONS,POST /admin/ratelimit/new/
ratelimit.delete_view               OPTIONS,POST         /admin/ratelimit/delete/
ratelimit.details_view              GET,HEAD,OPTIONS     /admin/ratelimit/details/
ratelimit.edit_view                 GET,HEAD,OPTIONS,POST /admin/ratelimit/edit/
ratelimit.export                    GET,HEAD,OPTIONS     /admin/ratelimit/export/<export_type>/
ratelimit.index_view                GET,HEAD,OPTIONS     /admin/ratelimit/

🔹 Blueprint: ratelimiter
-----------------------
ratelimiter.action_view             OPTIONS,POST         /admin/ratelimiter/action/
ratelimiter.ajax_lookup             GET,HEAD,OPTIONS     /admin/ratelimiter/ajax/lookup/
ratelimiter.ajax_update             OPTIONS,POST         /admin/ratelimiter/ajax/update/
ratelimiter.create_view             GET,HEAD,OPTIONS,POST /admin/ratelimiter/new/
ratelimiter.delete_view             OPTIONS,POST         /admin/ratelimiter/delete/
ratelimiter.details_view            GET,HEAD,OPTIONS     /admin/ratelimiter/details/
ratelimiter.edit_view               GET,HEAD,OPTIONS,POST /admin/ratelimiter/edit/
ratelimiter.export                  GET,HEAD,OPTIONS     /admin/ratelimiter/export/<export_type>/
ratelimiter.index_view              GET,HEAD,OPTIONS     /admin/ratelimiter/

🔹 Blueprint: referral
--------------------
referral.action_view                OPTIONS,POST         /admin/referral/action/
referral.ajax_lookup                GET,HEAD,OPTIONS     /admin/referral/ajax/lookup/
referral.ajax_update                OPTIONS,POST         /admin/referral/ajax/update/
referral.create_view                GET,HEAD,OPTIONS,POST /admin/referral/new/
referral.delete_view                OPTIONS,POST         /admin/referral/delete/
referral.details_view               GET,HEAD,OPTIONS     /admin/referral/details/
referral.edit_view                  GET,HEAD,OPTIONS,POST /admin/referral/edit/
referral.export                     GET,HEAD,OPTIONS     /admin/referral/export/<export_type>/
referral.index_view                 GET,HEAD,OPTIONS     /admin/referral/

🔹 Blueprint: report
------------------
report.action_view                  OPTIONS,POST         /admin/report/action/
report.ajax_lookup                  GET,HEAD,OPTIONS     /admin/report/ajax/lookup/
report.ajax_update                  OPTIONS,POST         /admin/report/ajax/update/
report.create_view                  GET,HEAD,OPTIONS,POST /admin/report/new/
report.delete_view                  OPTIONS,POST         /admin/report/delete/
report.details_view                 GET,HEAD,OPTIONS     /admin/report/details/
report.edit_view                    GET,HEAD,OPTIONS,POST /admin/report/edit/
report.export                       GET,HEAD,OPTIONS     /admin/report/export/<export_type>/
report.index_view                   GET,HEAD,OPTIONS     /admin/report/

🔹 Blueprint: reports
-------------------
reports.create_report               OPTIONS,POST         /api/reports/
reports.export_report               GET,HEAD,OPTIONS     /api/reports/export/<report_type>
reports.get_aging_report            GET,HEAD,OPTIONS     /api/reports/financial/aging
reports.get_appointment_summary     GET,HEAD,OPTIONS     /api/reports/appointments/summary
reports.get_financial_summary       GET,HEAD,OPTIONS     /api/reports/financial/summary
reports.get_no_show_report          GET,HEAD,OPTIONS     /api/reports/appointments/no-shows
reports.get_patient_activity_report GET,HEAD,OPTIONS     /api/reports/clinical/patient-activity
reports.get_reports                 GET,HEAD,OPTIONS     /api/reports/

🔹 Blueprint: role
----------------
role.action_view                    OPTIONS,POST         /admin/role/action/
role.ajax_lookup                    GET,HEAD,OPTIONS     /admin/role/ajax/lookup/
role.ajax_update                    OPTIONS,POST         /admin/role/ajax/update/
role.create_view                    GET,HEAD,OPTIONS,POST /admin/role/new/
role.delete_view                    OPTIONS,POST         /admin/role/delete/
role.details_view                   GET,HEAD,OPTIONS     /admin/role/details/
role.edit_view                      GET,HEAD,OPTIONS,POST /admin/role/edit/
role.export                         GET,HEAD,OPTIONS     /admin/role/export/<export_type>/
role.index_view                     GET,HEAD,OPTIONS     /admin/role/

🔹 Blueprint: settings
--------------------
settings.get_settings               GET,HEAD,OPTIONS     /api/settings/
settings.update_organization_settings OPTIONS,PUT          /api/settings/organization
settings.update_user_settings       OPTIONS,PUT          /api/settings/user

🔹 Blueprint: slotexception
-------------------------
slotexception.action_view           OPTIONS,POST         /admin/slotexception/action/
slotexception.ajax_lookup           GET,HEAD,OPTIONS     /admin/slotexception/ajax/lookup/
slotexception.ajax_update           OPTIONS,POST         /admin/slotexception/ajax/update/
slotexception.create_view           GET,HEAD,OPTIONS,POST /admin/slotexception/new/
slotexception.delete_view           OPTIONS,POST         /admin/slotexception/delete/
slotexception.details_view          GET,HEAD,OPTIONS     /admin/slotexception/details/
slotexception.edit_view             GET,HEAD,OPTIONS,POST /admin/slotexception/edit/
slotexception.export                GET,HEAD,OPTIONS     /admin/slotexception/export/<export_type>/
slotexception.index_view            GET,HEAD,OPTIONS     /admin/slotexception/

🔹 Blueprint: subscription
------------------------
subscription.action_view            OPTIONS,POST         /admin/subscription/action/
subscription.ajax_lookup            GET,HEAD,OPTIONS     /admin/subscription/ajax/lookup/
subscription.ajax_update            OPTIONS,POST         /admin/subscription/ajax/update/
subscription.create_view            GET,HEAD,OPTIONS,POST /admin/subscription/new/
subscription.delete_view            OPTIONS,POST         /admin/subscription/delete/
subscription.details_view           GET,HEAD,OPTIONS     /admin/subscription/details/
subscription.edit_view              GET,HEAD,OPTIONS,POST /admin/subscription/edit/
subscription.export                 GET,HEAD,OPTIONS     /admin/subscription/export/<export_type>/
subscription.index_view             GET,HEAD,OPTIONS     /admin/subscription/

🔹 Blueprint: supplier
--------------------
supplier.action_view                OPTIONS,POST         /admin/supplier/action/
supplier.ajax_lookup                GET,HEAD,OPTIONS     /admin/supplier/ajax/lookup/
supplier.ajax_update                OPTIONS,POST         /admin/supplier/ajax/update/
supplier.create_view                GET,HEAD,OPTIONS,POST /admin/supplier/new/
supplier.delete_view                OPTIONS,POST         /admin/supplier/delete/
supplier.details_view               GET,HEAD,OPTIONS     /admin/supplier/details/
supplier.edit_view                  GET,HEAD,OPTIONS,POST /admin/supplier/edit/
supplier.export                     GET,HEAD,OPTIONS     /admin/supplier/export/<export_type>/
supplier.index_view                 GET,HEAD,OPTIONS     /admin/supplier/

🔹 Blueprint: telehealthsession
-----------------------------
telehealthsession.action_view       OPTIONS,POST         /admin/telehealthsession/action/
telehealthsession.ajax_lookup       GET,HEAD,OPTIONS     /admin/telehealthsession/ajax/lookup/
telehealthsession.ajax_update       OPTIONS,POST         /admin/telehealthsession/ajax/update/
telehealthsession.create_view       GET,HEAD,OPTIONS,POST /admin/telehealthsession/new/
telehealthsession.delete_view       OPTIONS,POST         /admin/telehealthsession/delete/
telehealthsession.details_view      GET,HEAD,OPTIONS     /admin/telehealthsession/details/
telehealthsession.edit_view         GET,HEAD,OPTIONS,POST /admin/telehealthsession/edit/
telehealthsession.export            GET,HEAD,OPTIONS     /admin/telehealthsession/export/<export_type>/
telehealthsession.index_view        GET,HEAD,OPTIONS     /admin/telehealthsession/

🔹 Blueprint: telemedicine
------------------------
telemedicine.create_session         OPTIONS,POST         /api/telemedicine/sessions
telemedicine.get_sessions           GET,HEAD,OPTIONS     /api/telemedicine/sessions

🔹 Blueprint: treatmentplan
-------------------------
treatmentplan.action_view           OPTIONS,POST         /admin/treatmentplan/action/
treatmentplan.ajax_lookup           GET,HEAD,OPTIONS     /admin/treatmentplan/ajax/lookup/
treatmentplan.ajax_update           OPTIONS,POST         /admin/treatmentplan/ajax/update/
treatmentplan.create_view           GET,HEAD,OPTIONS,POST /admin/treatmentplan/new/
treatmentplan.delete_view           OPTIONS,POST         /admin/treatmentplan/delete/
treatmentplan.details_view          GET,HEAD,OPTIONS     /admin/treatmentplan/details/
treatmentplan.edit_view             GET,HEAD,OPTIONS,POST /admin/treatmentplan/edit/
treatmentplan.export                GET,HEAD,OPTIONS     /admin/treatmentplan/export/<export_type>/
treatmentplan.index_view            GET,HEAD,OPTIONS     /admin/treatmentplan/

🔹 Blueprint: treatmentroom
-------------------------
treatmentroom.action_view           OPTIONS,POST         /admin/treatmentroom/action/
treatmentroom.ajax_lookup           GET,HEAD,OPTIONS     /admin/treatmentroom/ajax/lookup/
treatmentroom.ajax_update           OPTIONS,POST         /admin/treatmentroom/ajax/update/
treatmentroom.create_view           GET,HEAD,OPTIONS,POST /admin/treatmentroom/new/
treatmentroom.delete_view           OPTIONS,POST         /admin/treatmentroom/delete/
treatmentroom.details_view          GET,HEAD,OPTIONS     /admin/treatmentroom/details/
treatmentroom.edit_view             GET,HEAD,OPTIONS,POST /admin/treatmentroom/edit/
treatmentroom.export                GET,HEAD,OPTIONS     /admin/treatmentroom/export/<export_type>/
treatmentroom.index_view            GET,HEAD,OPTIONS     /admin/treatmentroom/

🔹 Blueprint: user
----------------
user.action_view                    OPTIONS,POST         /admin/user/action/
user.ajax_lookup                    GET,HEAD,OPTIONS     /admin/user/ajax/lookup/
user.ajax_update                    OPTIONS,POST         /admin/user/ajax/update/
user.create_view                    GET,HEAD,OPTIONS,POST /admin/user/new/
user.delete_view                    OPTIONS,POST         /admin/user/delete/
user.details_view                   GET,HEAD,OPTIONS     /admin/user/details/
user.edit_view                      GET,HEAD,OPTIONS,POST /admin/user/edit/
user.export                         GET,HEAD,OPTIONS     /admin/user/export/<export_type>/
user.index_view                     GET,HEAD,OPTIONS     /admin/user/

🔹 Blueprint: users
-----------------
users.change_password               OPTIONS,PUT          /api/users/me/password
users.create_user                   OPTIONS,POST         /api/users/
users.delete_user                   DELETE,OPTIONS       /api/users/<int:user_id>
users.get_me                        GET,HEAD,OPTIONS     /api/users/me
users.get_profile                   GET,HEAD,OPTIONS     /api/users/<int:user_id>/profile
users.get_settings                  GET,HEAD,OPTIONS     /api/users/me/settings
users.get_user                      GET,HEAD,OPTIONS     /api/users/<int:user_id>
users.list_users                    GET,HEAD,OPTIONS     /api/users/
users.update_me                     OPTIONS,PUT          /api/users/me
users.update_settings               OPTIONS,PUT          /api/users/me/settings
users.update_user                   OPTIONS,PUT          /api/users/<int:user_id>

🔹 Blueprint: usersession
-----------------------
usersession.action_view             OPTIONS,POST         /admin/usersession/action/
usersession.ajax_lookup             GET,HEAD,OPTIONS     /admin/usersession/ajax/lookup/
usersession.ajax_update             OPTIONS,POST         /admin/usersession/ajax/update/
usersession.create_view             GET,HEAD,OPTIONS,POST /admin/usersession/new/
usersession.delete_view             OPTIONS,POST         /admin/usersession/delete/
usersession.details_view            GET,HEAD,OPTIONS     /admin/usersession/details/
usersession.edit_view               GET,HEAD,OPTIONS,POST /admin/usersession/edit/
usersession.export                  GET,HEAD,OPTIONS     /admin/usersession/export/<export_type>/
usersession.index_view              GET,HEAD,OPTIONS     /admin/usersession/

🔹 Blueprint: vitalsign
---------------------
vitalsign.action_view               OPTIONS,POST         /admin/vitalsign/action/
vitalsign.ajax_lookup               GET,HEAD,OPTIONS     /admin/vitalsign/ajax/lookup/
vitalsign.ajax_update               OPTIONS,POST         /admin/vitalsign/ajax/update/
vitalsign.create_view               GET,HEAD,OPTIONS,POST /admin/vitalsign/new/
vitalsign.delete_view               OPTIONS,POST         /admin/vitalsign/delete/
vitalsign.details_view              GET,HEAD,OPTIONS     /admin/vitalsign/details/
vitalsign.edit_view                 GET,HEAD,OPTIONS,POST /admin/vitalsign/edit/
vitalsign.export                    GET,HEAD,OPTIONS     /admin/vitalsign/export/<export_type>/
vitalsign.index_view                GET,HEAD,OPTIONS     /admin/vitalsign/

🔹 Blueprint: webhook
-------------------
webhook.action_view                 OPTIONS,POST         /admin/webhook/action/
webhook.ajax_lookup                 GET,HEAD,OPTIONS     /admin/webhook/ajax/lookup/
webhook.ajax_update                 OPTIONS,POST         /admin/webhook/ajax/update/
webhook.create_view                 GET,HEAD,OPTIONS,POST /admin/webhook/new/
webhook.delete_view                 OPTIONS,POST         /admin/webhook/delete/
webhook.details_view                GET,HEAD,OPTIONS     /admin/webhook/details/
webhook.edit_view                   GET,HEAD,OPTIONS,POST /admin/webhook/edit/
webhook.export                      GET,HEAD,OPTIONS     /admin/webhook/export/<export_type>/
webhook.index_view                  GET,HEAD,OPTIONS     /admin/webhook/

🔹 Blueprint: webhookevent
------------------------
webhookevent.action_view            OPTIONS,POST         /admin/webhookevent/action/
webhookevent.ajax_lookup            GET,HEAD,OPTIONS     /admin/webhookevent/ajax/lookup/
webhookevent.ajax_update            OPTIONS,POST         /admin/webhookevent/ajax/update/
webhookevent.create_view            GET,HEAD,OPTIONS,POST /admin/webhookevent/new/
webhookevent.delete_view            OPTIONS,POST         /admin/webhookevent/delete/
webhookevent.details_view           GET,HEAD,OPTIONS     /admin/webhookevent/details/
webhookevent.edit_view              GET,HEAD,OPTIONS,POST /admin/webhookevent/edit/
webhookevent.export                 GET,HEAD,OPTIONS     /admin/webhookevent/export/<export_type>/
webhookevent.index_view             GET,HEAD,OPTIONS     /admin/webhookevent/

🔹 Blueprint: widget
------------------
widget.action_view                  OPTIONS,POST         /admin/widget/action/
widget.ajax_lookup                  GET,HEAD,OPTIONS     /admin/widget/ajax/lookup/
widget.ajax_update                  OPTIONS,POST         /admin/widget/ajax/update/
widget.create_view                  GET,HEAD,OPTIONS,POST /admin/widget/new/
widget.delete_view                  OPTIONS,POST         /admin/widget/delete/
widget.details_view                 GET,HEAD,OPTIONS     /admin/widget/details/
widget.edit_view                    GET,HEAD,OPTIONS,POST /admin/widget/edit/
widget.export                       GET,HEAD,OPTIONS     /admin/widget/export/<export_type>/
widget.index_view                   GET,HEAD,OPTIONS     /admin/widget/

🔹 Blueprint: widget_api
----------------------
widget_api.create_widget            OPTIONS,POST         /api/widget/create
widget_api.get_widget               GET,HEAD,OPTIONS     /api/widget/data/<int:widget_id>
widget_api.get_widget_data          GET,HEAD,OPTIONS     /api/widget/data
widget_api.update_widget            OPTIONS,POST         /api/widget/update

🔹 Blueprint: widgettemplate
--------------------------
widgettemplate.action_view          OPTIONS,POST         /admin/widgettemplate/action/
widgettemplate.ajax_lookup          GET,HEAD,OPTIONS     /admin/widgettemplate/ajax/lookup/
widgettemplate.ajax_update          OPTIONS,POST         /admin/widgettemplate/ajax/update/
widgettemplate.create_view          GET,HEAD,OPTIONS,POST /admin/widgettemplate/new/
widgettemplate.delete_view          OPTIONS,POST         /admin/widgettemplate/delete/
widgettemplate.details_view         GET,HEAD,OPTIONS     /admin/widgettemplate/details/
widgettemplate.edit_view            GET,HEAD,OPTIONS,POST /admin/widgettemplate/edit/
widgettemplate.export               GET,HEAD,OPTIONS     /admin/widgettemplate/export/<export_type>/
widgettemplate.index_view           GET,HEAD,OPTIONS     /admin/widgettemplate/
(.venv) soji@soji-Aurora-R3:~/Documents/Projects/Dentaloist/backend$ 