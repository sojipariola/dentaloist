# Architecture (Phase 1 Extended)

## Overview
- Flask API with OpenAPI docs at `/docs` via Flask-Smorest.
- PostgreSQL DB. Soft multi-tenancy using `tenant_id` column.
- JWT contains `tenant_id` & `role` claims.
- Stripe used for subscription billing (checkout + webhook).
- Flask-Admin for quick administrative tasks in dev.

## RBAC
- Roles: `admin`, `clinic`, `lab`.
- Role is stored in JWT at login and used in decorators to protect endpoints.

## Billing Flow
1. User registers -> Stripe customer created (test)
2. User requests checkout session -> redirect to Stripe checkout
3. Stripe webhook updates subscription status

## Security
- Secure secrets via environment variables.
- Use HTTPS/Reverse proxy in production.



Endpoint                                       Methods         Rule                                                             
---------------------------------------------  --------------  -----------------------------------------------------------------
WebAuth.change_password                        GET, POST       /web/change-password                                             
WebAuth.forgot_password                        GET, POST       /web/forgot-password                                             
WebAuth.profile                                GET, POST       /web/profile                                                     
WebAuth.reset_password                         GET, POST       /web/reset-password/<token>                                      
WebAuth.security_settings                      GET, POST       /web/security                                                    
WebAuth.web_login                              GET, POST       /web/login                                                       
WebAuth.web_login_2fa                          GET, POST       /web/login/2fa                                                   
WebAuth.web_logout                             GET             /web/logout                                                      
admin.index                                    GET             /admin/                                                          
admin.login_view                               GET, POST       /admin/login/                                                    
admin.logout_view                              GET             /admin/logout/                                                   
admin.static                                   GET             /admin/static/<path:filename>                                    
analytics.get_appointment_analytics            GET             /api/analytics/appointments                                      
analytics.get_dashboard_analytics              GET             /api/analytics/dashboard                                         
analytics.get_patient_analytics                GET             /api/analytics/patients                                          
analytics.get_revenue_analytics                GET             /api/analytics/revenue                                           
api-docs.openapi_json                          GET             /openapi.json                                                    
api-docs.openapi_swagger_ui                    GET             /docs                                                            
appointment.action_view                        POST            /admin/appointment/action/                                       
appointment.ajax_lookup                        GET             /admin/appointment/ajax/lookup/                                  
appointment.ajax_update                        POST            /admin/appointment/ajax/update/                                  
appointment.create_view                        GET, POST       /admin/appointment/new/                                          
appointment.delete_view                        POST            /admin/appointment/delete/                                       
appointment.details_view                       GET             /admin/appointment/details/                                      
appointment.edit_view                          GET, POST       /admin/appointment/edit/                                         
appointment.export                             GET             /admin/appointment/export/<export_type>/                         
appointment.index_view                         GET             /admin/appointment/                                              
appointments.cancel_appointment                POST            /api/appointments/<int:appointment_id>/cancel                    
appointments.check_availability                GET             /api/appointments/availability                                   
appointments.complete_appointment              POST            /api/appointments/<int:appointment_id>/complete                  
appointments.create_appointment                POST            /api/appointments/                                               
appointments.delete_appointment                DELETE          /api/appointments/<int:appointment_id>                           
appointments.get_appointment                   GET             /api/appointments/<int:appointment_id>                           
appointments.get_appointments                  GET             /api/appointments/                                               
appointments.get_today_appointments            GET             /api/appointments/today                                          
appointments.get_upcoming_appointments         GET             /api/appointments/upcoming                                       
appointments.update_appointment                PUT             /api/appointments/<int:appointment_id>                           
audit.export_audit_logs                        GET             /api/audit/logs/export                                           
audit.get_audit_logs                           GET             /api/audit/logs                                                  
audit.get_audit_statistics                     GET             /api/audit/stats                                                 
audit.get_user_activity                        GET             /api/audit/users/<int:user_id>/activity                          
audit.manage_audit_config                      GET, PUT        /api/audit/config                                                
auth.change_password                           POST            /api/auth/change-password                                        
auth.forgot_password                           POST            /api/auth/forgot-password                                        
auth.get_current_user_route                    GET             /api/auth/me                                                     
auth.get_login_attempts_route                  GET             /api/auth/security/attempts                                      
auth.get_security_stats_route                  GET             /api/auth/security/stats                                         
auth.get_sessions                              GET             /api/auth/sessions                                               
auth.google_callback                           GET             /api/auth/google/callback                                        
auth.google_login                              GET             /api/auth/google/login                                           
auth.health_check                              GET             /api/auth/health                                                 
auth.login                                     POST            /api/auth/login                                                  
auth.login_form                                GET             /api/auth/login-form                                             
auth.logout_all_route                          POST            /api/auth/logout-all                                             
auth.logout_route                              POST            /api/auth/logout                                                 
auth.refresh_tokens                            POST            /api/auth/refresh                                                
auth.register                                  POST            /api/auth/register                                               
auth.reset_password                            POST            /api/auth/reset-password                                         
auth.revoke_session                            DELETE          /api/auth/sessions/<int:session_id>                              
billing.billing_dashboard                      GET             /api/billing/dashboard                                           
billing.create_insurance_claim                 POST            /api/billing/insurance-claims                                    
billing.create_invoice                         POST            /api/billing/invoices                                            
billing.create_payment                         POST            /api/billing/payments                                            
billing.delete_invoice                         DELETE          /api/billing/invoices/<int:invoice_id>                           
billing.delete_payment                         DELETE          /api/billing/payments/<int:payment_id>                           
billing.get_invoice                            GET             /api/billing/invoices/<int:invoice_id>                           
billing.get_invoices                           GET             /api/billing/invoices                                            
billing.update_insurance_claim                 PUT             /api/billing/insurance-claims/<int:claim_id>                     
billing.update_invoice                         PUT             /api/billing/invoices/<int:invoice_id>                           
clinical.create_medical_record                 POST            /api/clinical/records                                            
clinical.delete_medical_attachment             DELETE          /api/clinical/records/<int:record_id>/attachments/<attachment_id>
clinical.delete_medical_record                 DELETE          /api/clinical/records/<int:record_id>                            
clinical.get_medical_record                    GET             /api/clinical/records/<int:record_id>                            
clinical.get_medical_records                   GET             /api/clinical/records                                            
clinical.lock_medical_record                   POST            /api/clinical/records/<int:record_id>/lock                       
clinical.patient_clinical_dashboard            GET             /api/clinical/dashboard/patient/<int:patient_id>                 
clinical.search_clinical_data                  GET             /api/clinical/search                                             
clinical.update_medical_record                 PUT             /api/clinical/records/<int:record_id>                            
clinical.upload_medical_attachment             POST            /api/clinical/records/<int:record_id>/attachments                
dashboard.create_widget                        POST            /api/dashboard/widgets                                           
dashboard.delete_widget                        DELETE          /api/dashboard/widgets/<int:widget_id>                           
dashboard.get_appointment_stats                GET             /api/dashboard/data/appointment-stats                            
dashboard.get_dashboard_layout                 GET             /api/dashboard/layout                                            
dashboard.get_financial_overview               GET             /api/dashboard/data/financial-overview                           
dashboard.get_patient_metrics                  GET             /api/dashboard/data/patient-metrics                              
dashboard.get_widget_data                      GET             /api/dashboard/data/widget/<widget_type>                         
dashboard.get_widgets                          GET             /api/dashboard/widgets                                           
dashboard.reset_widgets                        POST            /api/dashboard/widgets/reset                                     
dashboard.update_dashboard_layout              PUT             /api/dashboard/layout                                            
dashboard.update_widget                        PUT             /api/dashboard/widgets/<int:widget_id>                           
family_members.create_family_member            POST            /api/family_members                                              
family_members.create_family_relationship      POST            /api/family_members/<int:fm_id>/relationships                    
family_members.delete_family_member            DELETE          /api/family_members/<int:fm_id>                                  
family_members.delete_family_relationship      DELETE          /api/family_members/relationships/<int:relationship_id>          
family_members.get_family_member               GET             /api/family_members/<int:fm_id>                                  
family_members.get_family_member_insurance     GET             /api/family_members/<int:fm_id>/insurance                        
family_members.get_family_relationships        GET             /api/family_members/<int:fm_id>/relationships                    
family_members.list_family_members             GET             /api/family_members                                              
family_members.update_family_member            PUT             /api/family_members/<int:fm_id>                                  
files.get_files                                GET             /api/files/                                                      
files.upload_file                              POST            /api/files/upload                                                
health                                         GET             /health                                                          
health.detailed_health                         GET             /api/health/detailed                                             
health.health_check                            GET             /api/health/                                                     
health.liveness_probe                          GET             /api/health/liveness                                             
health.metrics                                 GET             /api/health/metrics                                              
health.readiness_probe                         GET             /api/health/readiness                                            
health.status                                  GET             /api/health/status                                               
healthz                                        GET             /healthz                                                         
insurance.check_insurance_coverage             POST            /api/insurance/coverage/check                                    
insurance.create_insurance_plan                POST            /api/insurance/plans                                             
insurance.delete_insurance_plan                DELETE          /api/insurance/plans/<int:plan_id>                               
insurance.get_insurance_coverage               GET             /api/insurance/plans/<int:plan_id>/coverage                      
insurance.get_insurance_plan                   GET             /api/insurance/plans/<int:plan_id>                               
insurance.list_insurance_plans                 GET             /api/insurance/plans                                             
insurance.update_insurance_plan                PUT             /api/insurance/plans/<int:plan_id>                               
insurance.verify_insurance_plan                POST            /api/insurance/plans/<int:plan_id>/verify                        
integrations.create_update_integration         POST            /api/integrations/<integration_type>                             
integrations.create_webhook                    POST            /api/integrations/<integration_type>/webhooks                    
integrations.delete_integration                DELETE          /api/integrations/<integration_type>                             
integrations.get_integration_detail            GET             /api/integrations/<integration_type>                             
integrations.get_integration_webhooks          GET             /api/integrations/<integration_type>/webhooks                    
integrations.get_integrations                  GET             /api/integrations/                                               
integrations.init_oauth_integration            GET             /api/integrations/<integration_type>/oauth/init                  
integrations.oauth_callback                    GET             /api/integrations/<integration_type>/oauth/callback              
integrations.test_integration                  POST            /api/integrations/<integration_type>/test                        
integrations.trigger_sync                      POST            /api/integrations/<integration_type>/sync                        
inventory.create_inventory_item                POST            /api/inventory/items                                             
inventory.create_inventory_transaction         POST            /api/inventory/transactions                                      
inventory.delete_inventory_item                DELETE          /api/inventory/items/<int:item_id>                               
inventory.get_inventory_item                   GET             /api/inventory/items/<int:item_id>                               
inventory.get_inventory_items                  GET             /api/inventory/items                                             
inventory.get_inventory_summary                GET             /api/inventory/reports/summary                                   
inventory.get_inventory_transactions           GET             /api/inventory/transactions                                      
inventory.get_inventory_valuation              GET             /api/inventory/reports/valuation                                 
inventory.update_inventory_item                PUT             /api/inventory/items/<int:item_id>                               
invoice.action_view                            POST            /admin/invoice/action/                                           
invoice.ajax_lookup                            GET             /admin/invoice/ajax/lookup/                                      
invoice.ajax_update                            POST            /admin/invoice/ajax/update/                                      
invoice.create_view                            GET, POST       /admin/invoice/new/                                              
invoice.delete_view                            POST            /admin/invoice/delete/                                           
invoice.details_view                           GET             /admin/invoice/details/                                          
invoice.edit_view                              GET, POST       /admin/invoice/edit/                                             
invoice.export                                 GET             /admin/invoice/export/<export_type>/                             
invoice.index_view                             GET             /admin/invoice/                                                  
labs.add_lab_results                           POST            /api/labs/orders/<int:order_id>/results                          
labs.approve_lab_results                       POST            /api/labs/orders/<int:order_id>/approve                          
labs.create_lab_order                          POST            /api/labs/orders                                                 
labs.get_lab_order                             GET             /api/labs/orders/<int:order_id>                                  
labs.get_lab_orders                            GET             /api/labs/orders                                                 
labs.get_lab_stats                             GET             /api/labs/stats                                                  
labs.reject_lab_results                        POST            /api/labs/orders/<int:order_id>/reject                           
labs.update_lab_order                          PUT             /api/labs/orders/<int:order_id>                                  
labs.update_lab_order_status                   PUT             /api/labs/orders/<int:order_id>/status                           
notifications.bulk_notification_actions        POST            /api/notifications/bulk-action                                   
notifications.clear_all_notifications          POST            /api/notifications/clear-all                                     
notifications.get_notification                 GET             /api/notifications/<int:notification_id>                         
notifications.get_notification_statistics      GET             /api/notifications/stats                                         
notifications.get_notifications                GET             /api/notifications/                                              
notifications.manage_notification_preferences  GET, PUT        /api/notifications/preferences                                   
notifications.mark_all_as_read                 POST            /api/notifications/read-all                                      
notifications.mark_as_read                     POST            /api/notifications/<int:notification_id>/read                    
notifications.mark_as_unread                   POST            /api/notifications/<int:notification_id>/unread                  
notifications.send_notification                POST            /api/notifications/send                                          
organization.action_view                       POST            /admin/organization/action/                                      
organization.ajax_lookup                       GET             /admin/organization/ajax/lookup/                                 
organization.ajax_update                       POST            /admin/organization/ajax/update/                                 
organization.create_view                       GET, POST       /admin/organization/new/                                         
organization.delete_view                       POST            /admin/organization/delete/                                      
organization.details_view                      GET             /admin/organization/details/                                     
organization.edit_view                         GET, POST       /admin/organization/edit/                                        
organization.export                            GET             /admin/organization/export/<export_type>/                        
organization.index_view                        GET             /admin/organization/                                             
organizations.create_organization              POST            /api/organizations/                                              
organizations.delete_organization              DELETE          /api/organizations/<org_id>                                      
organizations.get_current_organization         GET             /api/organizations/current                                       
organizations.get_organization                 GET             /api/organizations/<org_id>                                      
organizations.get_organization_stats           GET             /api/organizations/<org_id>/stats                                
organizations.get_organization_users           GET             /api/organizations/<org_id>/users                                
organizations.get_organizations                GET             /api/organizations/                                              
organizations.manage_organization_settings     GET, PUT        /api/organizations/<org_id>/settings                             
organizations.update_organization              PUT             /api/organizations/<org_id>                                      
organizations.update_subscription              PUT             /api/organizations/<org_id>/subscription                         
patient.action_view                            POST            /admin/patient/action/                                           
patient.ajax_lookup                            GET             /admin/patient/ajax/lookup/                                      
patient.ajax_update                            POST            /admin/patient/ajax/update/                                      
patient.create_view                            GET, POST       /admin/patient/new/                                              
patient.delete_view                            POST            /admin/patient/delete/                                           
patient.details_view                           GET             /admin/patient/details/                                          
patient.edit_view                              GET, POST       /admin/patient/edit/                                             
patient.export                                 GET             /admin/patient/export/<export_type>/                             
patient.index_view                             GET             /admin/patient/                                                  
patients.create_patient                        POST            /api/patients/                                                   
patients.delete_patient                        DELETE          /api/patients/<int:patient_id>                                   
patients.get_patient                           GET             /api/patients/<int:patient_id>                                   
patients.get_patient_statistics                GET             /api/patients/stats                                              
patients.get_patients                          GET             /api/patients/                                                   
patients.import_patients                       POST            /api/patients/import                                             
patients.manage_medical_history                GET, POST, PUT  /api/patients/<int:patient_id>/medical-history                   
patients.reactivate_patient                    POST            /api/patients/<int:patient_id>/reactivate                        
patients.update_patient                        PUT             /api/patients/<int:patient_id>                                   
payment.action_view                            POST            /admin/payment/action/                                           
payment.ajax_lookup                            GET             /admin/payment/ajax/lookup/                                      
payment.ajax_update                            POST            /admin/payment/ajax/update/                                      
payment.create_view                            GET, POST       /admin/payment/new/                                              
payment.delete_view                            POST            /admin/payment/delete/                                           
payment.details_view                           GET             /admin/payment/details/                                          
payment.edit_view                              GET, POST       /admin/payment/edit/                                             
payment.export                                 GET             /admin/payment/export/<export_type>/                             
payment.index_view                             GET             /admin/payment/                                                  
prescriptions.approve_prescription             POST            /api/prescriptions/<int:prescription_id>/approve                 
prescriptions.cancel_prescription              POST            /api/prescriptions/<int:prescription_id>/cancel                  
prescriptions.create_prescription              POST            /api/prescriptions/                                              
prescriptions.delete_prescription              DELETE          /api/prescriptions/<int:prescription_id>                         
prescriptions.dispense_prescription            POST            /api/prescriptions/<int:prescription_id>/dispense                
prescriptions.get_patient_prescriptions        GET             /api/prescriptions/patient/<int:patient_id>                      
prescriptions.get_prescription                 GET             /api/prescriptions/<int:prescription_id>                         
prescriptions.get_prescription_statistics      GET             /api/prescriptions/stats                                         
prescriptions.get_prescriptions                GET             /api/prescriptions/                                              
prescriptions.update_prescription              PUT             /api/prescriptions/<int:prescription_id>                         
reports.create_analytics_report                POST            /api/reports/analytics                                           
reports.create_financial_report                POST            /api/reports/financial                                           
reports.export_analytics_report                GET             /api/reports/analytics/export                                    
reports.export_financial_report                GET             /api/reports/financial/export                                    
reports.get_aging_report                       GET             /api/reports/financial/aging                                     
reports.get_analytics_reports                  GET             /api/reports/analytics                                           
reports.get_appointment_analytics              GET             /api/reports/analytics/appointments                              
reports.get_financial_reports                  GET             /api/reports/financial                                           
reports.get_financial_summary                  GET             /api/reports/financial/summary                                   
reports.get_patient_activity_analytics         GET             /api/reports/analytics/patient-activity                          
role.action_view                               POST            /admin/role/action/                                              
role.ajax_lookup                               GET             /admin/role/ajax/lookup/                                         
role.ajax_update                               POST            /admin/role/ajax/update/                                         
role.create_view                               GET, POST       /admin/role/new/                                                 
role.delete_view                               POST            /admin/role/delete/                                              
role.details_view                              GET             /admin/role/details/                                             
role.edit_view                                 GET, POST       /admin/role/edit/                                                
role.export                                    GET             /admin/role/export/<export_type>/                                
role.index_view                                GET             /admin/role/                                                     
root                                           GET             /                                                                
settings.get_settings                          GET             /api/settings/                                                   
settings.get_settings_audit_log                GET             /api/settings/audit                                              
settings.manage_notification_settings          GET, PUT        /api/settings/notifications                                      
settings.manage_organization_settings          GET, PUT        /api/settings/organization                                       
settings.manage_practice_settings              GET, PUT        /api/settings/organization/practice                              
settings.manage_user_preferences               GET, PUT        /api/settings/preferences                                        
settings.manage_user_settings                  GET, PUT        /api/settings/user                                               
settings.reset_organization_settings           POST            /api/settings/reset/organization                                 
settings.reset_user_settings                   POST            /api/settings/reset/user                                         
static                                         GET             /static/<path:filename>                                          
telemedicine.cancel_session                    POST            /api/telemedicine/sessions/<int:session_id>/cancel               
telemedicine.check_availability                GET             /api/telemedicine/availability                                   
telemedicine.create_session                    POST            /api/telemedicine/sessions                                       
telemedicine.end_session                       POST            /api/telemedicine/sessions/<int:session_id>/end                  
telemedicine.get_session                       GET             /api/telemedicine/sessions/<int:session_id>                      
telemedicine.get_sessions                      GET             /api/telemedicine/sessions                                       
telemedicine.get_telehealth_statistics         GET             /api/telemedicine/stats                                          
telemedicine.join_session                      POST            /api/telemedicine/sessions/<int:session_id>/join                 
telemedicine.start_session                     POST            /api/telemedicine/sessions/<int:session_id>/start                
telemedicine.update_session                    PUT             /api/telemedicine/sessions/<int:session_id>                      
tenant.action_view                             POST            /admin/tenant/action/                                            
tenant.ajax_lookup                             GET             /admin/tenant/ajax/lookup/                                       
tenant.ajax_update                             POST            /admin/tenant/ajax/update/                                       
tenant.create_view                             GET, POST       /admin/tenant/new/                                               
tenant.delete_view                             POST            /admin/tenant/delete/                                            
tenant.details_view                            GET             /admin/tenant/details/                                           
tenant.edit_view                               GET, POST       /admin/tenant/edit/                                              
tenant.export                                  GET             /admin/tenant/export/<export_type>/                              
tenant.index_view                              GET             /admin/tenant/                                                   
treatment.action_view                          POST            /admin/treatment/action/                                         
treatment.ajax_lookup                          GET             /admin/treatment/ajax/lookup/                                    
treatment.ajax_update                          POST            /admin/treatment/ajax/update/                                    
treatment.create_view                          GET, POST       /admin/treatment/new/                                            
treatment.delete_view                          POST            /admin/treatment/delete/                                         
treatment.details_view                         GET             /admin/treatment/details/                                        
treatment.edit_view                            GET, POST       /admin/treatment/edit/                                           
treatment.export                               GET             /admin/treatment/export/<export_type>/                           
treatment.index_view                           GET             /admin/treatment/                                                
user.action_view                               POST            /admin/user/action/                                              
user.ajax_lookup                               GET             /admin/user/ajax/lookup/                                         
user.ajax_update                               POST            /admin/user/ajax/update/                                         
user.create_view                               GET, POST       /admin/user/new/                                                 
user.delete_view                               POST            /admin/user/delete/                                              
user.details_view                              GET             /admin/user/details/                                             
user.edit_view                                 GET, POST       /admin/user/edit/                                                
user.export                                    GET             /admin/user/export/<export_type>/                                
user.index_view                                GET             /admin/user/                                                     
users.change_password                          PUT             /api/users/me/password                                           
users.create_user                              POST            /api/users/                                                      
users.delete_user                              DELETE          /api/users/<int:user_id>                                         
users.get_me                                   GET             /api/users/me                                                    
users.get_profile                              GET             /api/users/<int:user_id>/profile                                 
users.get_settings                             GET             /api/users/me/settings                                           
users.get_user                                 GET             /api/users/<int:user_id>                                         
users.list_users                               GET             /api/users/                                                      
users.update_me                                PUT             /api/users/me                                                    
users.update_settings                          PUT             /api/users/me/settings                                           
users.update_user                              PUT             /api/users/<int:user_id>                                         
widget_api.get_available_widgets               GET             /api/widget/available                                            
widget_api.get_dashboard_widgets               GET             /api/widget/dashboard                                            
widget_api.get_widget_data                     GET             /api/widget/<widget_id>/data                                     
widget_api.manage_dashboard_layout             GET, PUT        /api/widget/layout                                               
widget_api.manage_widget_config                POST, PUT       /api/widget/config                                               
widget_api.refresh_widgets                     POST            /api/widget/refresh                                              
widget_api.remove_widget                       DELETE          /api/widget/<widget_id> 