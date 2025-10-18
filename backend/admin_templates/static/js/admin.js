
// Admin Interface JavaScript
const schemaInfo = {
  "tables": {
    "allergies": {
      "category": "System",
      "columns": [
        {
          "name": "patient_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "allergen",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "reaction",
          "type": "VARCHAR(255)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "severity_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "onset_date",
          "type": "DATE",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "notes",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "recorded_by",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "patient_id"
          ],
          "references": "patients.['id']",
          "name": null
        },
        {
          "columns": [
            "severity_id"
          ],
          "references": "allergy_severities.['id']",
          "name": null
        },
        {
          "columns": [
            "recorded_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_allergy_allergen",
          "columns": [
            "allergen"
          ],
          "unique": 0
        },
        {
          "name": "idx_allergy_patient",
          "columns": [
            "patient_id",
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "allergy_severities": {
      "category": "System",
      "columns": [
        {
          "name": "requires_emergency_care",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "risk_level",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_allergy_severities_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_allergy_severities_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 4
    },
    "analytics_dashboards": {
      "category": "Analytics",
      "columns": [
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "layout_type",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_default",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_public",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "refresh_interval",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "allowed_roles",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "required_permissions",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "theme",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "custom_css",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_dashboard_org_default",
          "columns": [
            "organization_id",
            "is_default"
          ],
          "unique": 0
        },
        {
          "name": "idx_dashboard_visibility",
          "columns": [
            "is_public",
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_analytics_dashboards_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "analytics_widgets": {
      "category": "Analytics",
      "columns": [
        {
          "name": "dashboard_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "title",
          "type": "VARCHAR(200)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "widget_type_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "data_source",
          "type": "VARCHAR(200)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "query_parameters",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "refresh_interval",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "position_x",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "position_y",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "width",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "height",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "configuration",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "filters",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_visible",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_enabled",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "cached_data",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "cached_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "cache_ttl",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "dashboard_id"
          ],
          "references": "analytics_dashboards.['id']",
          "name": null
        },
        {
          "columns": [
            "widget_type_id"
          ],
          "references": "widget_types.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_widget_dashboard",
          "columns": [
            "dashboard_id"
          ],
          "unique": 0
        },
        {
          "name": "idx_widget_type",
          "columns": [
            "widget_type_id"
          ],
          "unique": 0
        },
        {
          "name": "idx_widget_visibility",
          "columns": [
            "is_visible",
            "is_enabled"
          ],
          "unique": 0
        },
        {
          "name": "ix_analytics_widgets_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "appointment_statuses": {
      "category": "Appointments",
      "columns": [
        {
          "name": "name",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "allows_editing",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_final_status",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_appointment_statuses_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_appointment_statuses_name",
          "columns": [
            "name"
          ],
          "unique": 1
        }
      ],
      "row_count": 7
    },
    "appointment_types": {
      "category": "Appointments",
      "columns": [
        {
          "name": "default_duration",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_specialist",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_appointment_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_appointment_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 12
    },
    "claim_statuses": {
      "category": "Financial",
      "columns": [
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_action",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "allows_resubmission",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_claim_statuses_code",
          "columns": [
            "code"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "currencies": {
      "category": "System",
      "columns": [
        {
          "name": "symbol",
          "type": "VARCHAR(10)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(3)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "decimal_places",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [],
      "row_count": 0
    },
    "email_logs": {
      "category": "System",
      "columns": [
        {
          "name": "recipient_email",
          "type": "VARCHAR(255)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "recipient_name",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "subject",
          "type": "VARCHAR(255)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "body",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "body_html",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sender_email",
          "type": "VARCHAR(255)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sender_name",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "template_id",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "email_type",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status_message",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "provider",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "provider_message_id",
          "type": "VARCHAR(255)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sent_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "delivered_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "opened_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "headers",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "attachments_count",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "retry_count",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "idx_email_log_recipient",
          "columns": [
            "recipient_email"
          ],
          "unique": 0
        },
        {
          "name": "idx_email_log_sent_at",
          "columns": [
            "sent_at"
          ],
          "unique": 0
        },
        {
          "name": "idx_email_log_status",
          "columns": [
            "status"
          ],
          "unique": 0
        },
        {
          "name": "idx_email_log_type",
          "columns": [
            "email_type"
          ],
          "unique": 0
        },
        {
          "name": "ix_email_logs_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_email_logs_recipient_email",
          "columns": [
            "recipient_email"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "expense_categories": {
      "category": "System",
      "columns": [
        {
          "name": "is_tax_deductible",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_approval",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "budget_category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_expense_categories_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_expense_categories_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "expenses": {
      "category": "System",
      "columns": [
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "category_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "payment_method_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "amount",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "expense_date",
          "type": "DATE",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "vendor_name",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "vendor_invoice_number",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "payment_date",
          "type": "DATE",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_recurring",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "recurrence_pattern",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_tax_deductible",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "tax_amount",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "approved_by",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "approved_date",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "incurred_by",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "category_id"
          ],
          "references": "expense_categories.['id']",
          "name": null
        },
        {
          "columns": [
            "payment_method_id"
          ],
          "references": "payment_methods.['id']",
          "name": null
        },
        {
          "columns": [
            "approved_by"
          ],
          "references": "users.['id']",
          "name": null
        },
        {
          "columns": [
            "incurred_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_expense_date",
          "columns": [
            "expense_date"
          ],
          "unique": 0
        },
        {
          "name": "idx_expense_org_category",
          "columns": [
            "organization_id",
            "category_id"
          ],
          "unique": 0
        },
        {
          "name": "idx_expense_status",
          "columns": [
            "status"
          ],
          "unique": 0
        },
        {
          "name": "idx_expense_vendor",
          "columns": [
            "vendor_name"
          ],
          "unique": 0
        },
        {
          "name": "ix_expenses_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "family_members": {
      "category": "System",
      "columns": [
        {
          "name": "user_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "patient_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "family_user_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_by",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "first_name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "last_name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "relationship_type",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "emergency_contact",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "primary_contact",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "user_id"
          ],
          "references": "users.['id']",
          "name": null
        },
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "patient_id"
          ],
          "references": "patients.['id']",
          "name": null
        },
        {
          "columns": [
            "family_user_id"
          ],
          "references": "users.['id']",
          "name": null
        },
        {
          "columns": [
            "created_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "ix_family_members_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "financial_reports": {
      "category": "Analytics",
      "columns": [
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "title",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "report_type",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "parameters",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "data",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "summary",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "generated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "period_start",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "period_end",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "file_url",
          "type": "VARCHAR(255)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_template",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_public",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "shared_with",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_by",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "created_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_financial_idx_report_created",
          "columns": [
            "created_at"
          ],
          "unique": 0
        },
        {
          "name": "idx_financial_report_org_type",
          "columns": [
            "organization_id",
            "report_type"
          ],
          "unique": 0
        },
        {
          "name": "idx_report_period",
          "columns": [
            "period_start",
            "period_end"
          ],
          "unique": 0
        },
        {
          "name": "ix_financial_reports_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "genders": {
      "category": "System",
      "columns": [
        {
          "name": "pronoun",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_genders_code",
          "columns": [
            "code"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "industry_types": {
      "category": "Lookup Tables",
      "columns": [
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_license",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "special_requirements",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_industry_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_industry_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "integration_statuses": {
      "category": "Lookup Tables",
      "columns": [
        {
          "name": "allows_sync",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_attention",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "retry_allowed",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_integration_statuses_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_integration_statuses_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "inventory_adjustment_types": {
      "category": "Inventory",
      "columns": [
        {
          "name": "stock_impact",
          "type": "VARCHAR(10)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_reason",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_approval",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_inventory_adjustment_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_inventory_adjustment_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "inventory_adjustments": {
      "category": "Inventory",
      "columns": [
        {
          "name": "item_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "adjustment_type_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "quantity",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "reason",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "adjusted_by",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "adjustment_date",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "item_id"
          ],
          "references": "inventory_items.['id']",
          "name": null
        },
        {
          "columns": [
            "adjustment_type_id"
          ],
          "references": "inventory_adjustment_types.['id']",
          "name": null
        },
        {
          "columns": [
            "adjusted_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_inventory_adj_item_date",
          "columns": [
            "item_id",
            "adjustment_date"
          ],
          "unique": 0
        },
        {
          "name": "idx_inventory_adj_type",
          "columns": [
            "adjustment_type_id"
          ],
          "unique": 0
        },
        {
          "name": "ix_inventory_adjustments_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "inventory_items": {
      "category": "Inventory",
      "columns": [
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(200)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "category",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sku",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "unit_price",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "quantity",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "min_quantity",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_quantity",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "cost",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "price",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "supplier_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "location",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "reorder_point",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "lead_time_days",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "supplier_id"
          ],
          "references": "suppliers.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_inventory_item_category",
          "columns": [
            "category"
          ],
          "unique": 0
        },
        {
          "name": "idx_inventory_item_name",
          "columns": [
            "name"
          ],
          "unique": 0
        },
        {
          "name": "idx_inventory_item_org_sku",
          "columns": [
            "organization_id",
            "sku"
          ],
          "unique": 0
        },
        {
          "name": "ix_inventory_items_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_inventory_items_name",
          "columns": [
            "name"
          ],
          "unique": 0
        },
        {
          "name": "ix_inventory_items_sku",
          "columns": [
            "sku"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "inventory_transaction_types": {
      "category": "Inventory",
      "columns": [
        {
          "name": "affects_stock",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "stock_direction",
          "type": "VARCHAR(10)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_approval",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_inventory_transaction_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_inventory_transaction_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "inventory_transactions": {
      "category": "Inventory",
      "columns": [
        {
          "name": "item_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "transaction_type_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "quantity",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "product_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "old_stock_level",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "new_stock_level",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "unit_cost",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "total_cost",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "reference_type",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "reference_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "notes",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "performed_by",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "item_id"
          ],
          "references": "inventory_items.['id']",
          "name": null
        },
        {
          "columns": [
            "transaction_type_id"
          ],
          "references": "inventory_transaction_types.['id']",
          "name": null
        },
        {
          "columns": [
            "product_id"
          ],
          "references": "products.['id']",
          "name": null
        },
        {
          "columns": [
            "performed_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_inventory_txn_item_date",
          "columns": [
            "item_id",
            "created_at"
          ],
          "unique": 0
        },
        {
          "name": "idx_inventory_txn_reference",
          "columns": [
            "reference_type",
            "reference_id"
          ],
          "unique": 0
        },
        {
          "name": "idx_inventory_txn_type",
          "columns": [
            "transaction_type_id"
          ],
          "unique": 0
        },
        {
          "name": "ix_inventory_transactions_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "invoice_statuses": {
      "category": "Financial",
      "columns": [
        {
          "name": "is_final",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "allows_editing",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "send_notifications",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_invoice_statuses_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_invoice_statuses_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "kpi_history": {
      "category": "Analytics",
      "columns": [
        {
          "name": "kpi_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "value",
          "type": "FLOAT",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "calculated_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "period_start",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "period_end",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "data_points",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "confidence_score",
          "type": "FLOAT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "kpi_id"
          ],
          "references": "kpis.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_kpi_history_kpi_date",
          "columns": [
            "kpi_id",
            "calculated_at"
          ],
          "unique": 0
        },
        {
          "name": "idx_kpi_history_period",
          "columns": [
            "period_start",
            "period_end"
          ],
          "unique": 0
        },
        {
          "name": "ix_kpi_history_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "kpis": {
      "category": "Analytics",
      "columns": [
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "calculation_query",
          "type": "TEXT",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "target_value",
          "type": "FLOAT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "target_type",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "target_range_min",
          "type": "FLOAT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "target_range_max",
          "type": "FLOAT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "unit",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "format_type",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "decimal_places",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "alert_enabled",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "alert_condition",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "alert_threshold",
          "type": "FLOAT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_kpi_alert",
          "columns": [
            "alert_enabled",
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "idx_kpi_org_category",
          "columns": [
            "organization_id",
            "category"
          ],
          "unique": 0
        },
        {
          "name": "ix_kpis_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "login_attempts": {
      "category": "System",
      "columns": [
        {
          "name": "user_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "username",
          "type": "VARCHAR(255)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "ip_address",
          "type": "VARCHAR(45)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "user_agent",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "success",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "attempt_type",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "failure_reason",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "user_id"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "ix_login_attempts_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "medication_routes": {
      "category": "System",
      "columns": [
        {
          "name": "administration_instructions",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_training",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_medication_routes_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_medication_routes_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 5
    },
    "note_types": {
      "category": "Lookup Tables",
      "columns": [
        {
          "name": "requires_soap_format",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "template",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_note_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_note_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 6
    },
    "notes": {
      "category": "System",
      "columns": [
        {
          "name": "patient_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_by",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "content",
          "type": "TEXT",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "tags",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "patient_id"
          ],
          "references": "patients.['id']",
          "name": null
        },
        {
          "columns": [
            "created_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "ix_notes_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "notification_types": {
      "category": "Lookup Tables",
      "columns": [
        {
          "name": "priority",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "auto_expire_days",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_action",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "template",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_notification_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_notification_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "organization_types": {
      "category": "Lookup Tables",
      "columns": [
        {
          "name": "max_users",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_patients",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "features_available",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_verification",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_organization_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_organization_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "organizations": {
      "category": "System",
      "columns": [
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "address",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "city",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "state",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "postal_code",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "country",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "phone",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "email",
          "type": "VARCHAR(120)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "website",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "organization_type_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "tax_id",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "business_type",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "industry",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_staff",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_patients",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_verified",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "tenant_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_type_id"
          ],
          "references": "organization_types.['id']",
          "name": null
        },
        {
          "columns": [
            "tenant_id"
          ],
          "references": "tenants.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_organization_email",
          "columns": [
            "email"
          ],
          "unique": 0
        },
        {
          "name": "idx_organization_status",
          "columns": [
            "status"
          ],
          "unique": 0
        },
        {
          "name": "idx_organization_tenant",
          "columns": [
            "tenant_id",
            "name"
          ],
          "unique": 0
        },
        {
          "name": "idx_organization_type",
          "columns": [
            "organization_type_id"
          ],
          "unique": 0
        },
        {
          "name": "ix_organizations_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_organizations_name",
          "columns": [
            "name"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "password_history": {
      "category": "System",
      "columns": [
        {
          "name": "user_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "password_hash",
          "type": "VARCHAR(255)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "user_id"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "ix_password_history_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "patients": {
      "category": "Clinical Data",
      "columns": [
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "first_name",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "last_name",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "email",
          "type": "VARCHAR(120)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "phone",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "date_of_birth",
          "type": "DATE",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "gender",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "address",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "emergency_contact",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "medical_history",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "allergies",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "medications",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "insurance_info",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "dental_history",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "oral_hygiene",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "last_dental_visit",
          "type": "DATE",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "next_recall_date",
          "type": "DATE",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "preferred_language",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "communication_preferences",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_patient_dob",
          "columns": [
            "date_of_birth"
          ],
          "unique": 0
        },
        {
          "name": "idx_patient_email",
          "columns": [
            "email"
          ],
          "unique": 0
        },
        {
          "name": "idx_patient_org_name",
          "columns": [
            "organization_id",
            "last_name",
            "first_name"
          ],
          "unique": 0
        },
        {
          "name": "idx_patient_status",
          "columns": [
            "status"
          ],
          "unique": 0
        },
        {
          "name": "ix_patients_date_of_birth",
          "columns": [
            "date_of_birth"
          ],
          "unique": 0
        },
        {
          "name": "ix_patients_email",
          "columns": [
            "email"
          ],
          "unique": 0
        },
        {
          "name": "ix_patients_first_name",
          "columns": [
            "first_name"
          ],
          "unique": 0
        },
        {
          "name": "ix_patients_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_patients_last_name",
          "columns": [
            "last_name"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "payment_methods": {
      "category": "Financial",
      "columns": [
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_processing",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "processing_fee_percentage",
          "type": "NUMERIC(5, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_online",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_payment_methods_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_payment_methods_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "payment_statuses": {
      "category": "Financial",
      "columns": [
        {
          "name": "is_completed",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "allows_refund",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_action",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_payment_statuses_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_payment_statuses_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "permission_categories": {
      "category": "User Management",
      "columns": [
        {
          "name": "module",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_permission_categories_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_permission_categories_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "permissions": {
      "category": "User Management",
      "columns": [
        {
          "name": "name",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "VARCHAR(255)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "idx_permission_category",
          "columns": [
            "category"
          ],
          "unique": 0
        },
        {
          "name": "idx_permission_name",
          "columns": [
            "name"
          ],
          "unique": 0
        },
        {
          "name": "ix_permissions_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_permissions_name",
          "columns": [
            "name"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "priority_levels": {
      "category": "System",
      "columns": [
        {
          "name": "escalation_hours",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_immediate_attention",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_priority_levels_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_priority_levels_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 4
    },
    "product_categories": {
      "category": "Inventory",
      "columns": [
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "parent_category_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "parent_category_id"
          ],
          "references": "product_categories.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_category_org_name",
          "columns": [
            "organization_id",
            "name"
          ],
          "unique": 0
        },
        {
          "name": "idx_category_parent",
          "columns": [
            "parent_category_id"
          ],
          "unique": 0
        },
        {
          "name": "ix_product_categories_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_product_categories_name",
          "columns": [
            "name"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "product_images": {
      "category": "Inventory",
      "columns": [
        {
          "name": "product_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "image_url",
          "type": "VARCHAR(500)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "caption",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_primary",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "product_id"
          ],
          "references": "products.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_product_image_primary",
          "columns": [
            "is_primary"
          ],
          "unique": 0
        },
        {
          "name": "idx_product_image_product",
          "columns": [
            "product_id"
          ],
          "unique": 0
        },
        {
          "name": "ix_product_images_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "product_price_history": {
      "category": "Inventory",
      "columns": [
        {
          "name": "product_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "old_price",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "new_price",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "changed_by",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "change_reason",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "effective_date",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "product_id"
          ],
          "references": "products.['id']",
          "name": null
        },
        {
          "columns": [
            "changed_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_price_history_date",
          "columns": [
            "effective_date"
          ],
          "unique": 0
        },
        {
          "name": "idx_price_history_product",
          "columns": [
            "product_id"
          ],
          "unique": 0
        },
        {
          "name": "ix_product_price_history_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "product_types": {
      "category": "Inventory",
      "columns": [
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_lot_tracking",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_expiration",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_medical",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_product_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_product_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "products": {
      "category": "Inventory",
      "columns": [
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "supplier_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "category_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "product_type_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sku",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(200)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "brand",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "model",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "unit_of_measure",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "unit_size",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "weight",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "dimensions",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "cost_price",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "selling_price",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "current_price",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "tax_rate",
          "type": "NUMERIC(5, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "discount_percentage",
          "type": "NUMERIC(5, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "min_stock_level",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_stock_level",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "reorder_point",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "current_stock",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "reserved_stock",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "average_consumption",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_medical",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_prescription",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "active_ingredients",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "dosage_form",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "strength",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "expiration_alert_days",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "shelf_life_months",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_refrigeration",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_taxable",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_returnable",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "return_period_days",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "barcode",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "manufacturer_code",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "supplier_code",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "ndc_code",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "supplier_id"
          ],
          "references": "suppliers.['id']",
          "name": null
        },
        {
          "columns": [
            "category_id"
          ],
          "references": "product_categories.['id']",
          "name": null
        },
        {
          "columns": [
            "product_type_id"
          ],
          "references": "product_types.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_product_barcode",
          "columns": [
            "barcode"
          ],
          "unique": 0
        },
        {
          "name": "idx_product_name_org",
          "columns": [
            "name",
            "organization_id"
          ],
          "unique": 0
        },
        {
          "name": "idx_product_sku_org",
          "columns": [
            "sku",
            "organization_id"
          ],
          "unique": 0
        },
        {
          "name": "idx_product_stock_level",
          "columns": [
            "current_stock"
          ],
          "unique": 0
        },
        {
          "name": "idx_product_type_status",
          "columns": [
            "product_type_id",
            "status"
          ],
          "unique": 0
        },
        {
          "name": "ix_products_barcode",
          "columns": [
            "barcode"
          ],
          "unique": 1
        },
        {
          "name": "ix_products_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_products_name",
          "columns": [
            "name"
          ],
          "unique": 0
        },
        {
          "name": "ix_products_sku",
          "columns": [
            "sku"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "purchase_order_statuses": {
      "category": "Inventory",
      "columns": [
        {
          "name": "allows_editing",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_final",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "send_notifications",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_purchase_order_statuses_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_purchase_order_statuses_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "purchase_orders": {
      "category": "Inventory",
      "columns": [
        {
          "name": "supplier_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "po_number",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "order_date",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "expected_delivery_date",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "actual_delivery_date",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "tracking_number",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "shipping_method",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "subtotal",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "tax_amount",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "shipping_cost",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "total_amount",
          "type": "NUMERIC(10, 2)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "notes",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "terms_and_conditions",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_by",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "approved_by",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "approved_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "supplier_id"
          ],
          "references": "suppliers.['id']",
          "name": null
        },
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "status_id"
          ],
          "references": "purchase_order_statuses.['id']",
          "name": null
        },
        {
          "columns": [
            "created_by"
          ],
          "references": "users.['id']",
          "name": null
        },
        {
          "columns": [
            "approved_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_po_delivery_date",
          "columns": [
            "expected_delivery_date"
          ],
          "unique": 0
        },
        {
          "name": "idx_po_number",
          "columns": [
            "po_number"
          ],
          "unique": 0
        },
        {
          "name": "idx_po_org_status",
          "columns": [
            "organization_id",
            "status_id"
          ],
          "unique": 0
        },
        {
          "name": "idx_po_supplier_date",
          "columns": [
            "supplier_id",
            "order_date"
          ],
          "unique": 0
        },
        {
          "name": "ix_purchase_orders_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_purchase_orders_po_number",
          "columns": [
            "po_number"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "rate_limits": {
      "category": "System",
      "columns": [
        {
          "name": "key",
          "type": "VARCHAR(255)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "timestamp",
          "type": "FLOAT",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "expires_at",
          "type": "FLOAT",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "idx_analytics_idx_rate_limit_expires_at",
          "columns": [
            "expires_at"
          ],
          "unique": 0
        },
        {
          "name": "idx_analytics_idx_rate_limit_key_timestamp",
          "columns": [
            "key",
            "timestamp"
          ],
          "unique": 0
        },
        {
          "name": "ix_rate_limits_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_rate_limits_key",
          "columns": [
            "key"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "report_runs": {
      "category": "Analytics",
      "columns": [
        {
          "name": "schedule_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "started_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "completed_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "duration_seconds",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "file_url",
          "type": "VARCHAR(500)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "file_size",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "record_count",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "error_message",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "stack_trace",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "schedule_id"
          ],
          "references": "report_schedules.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_report_run_schedule",
          "columns": [
            "schedule_id",
            "created_at"
          ],
          "unique": 0
        },
        {
          "name": "idx_report_run_status",
          "columns": [
            "status",
            "created_at"
          ],
          "unique": 0
        },
        {
          "name": "ix_report_runs_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "report_schedules": {
      "category": "Analytics",
      "columns": [
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "report_type_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "parameters",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "output_format",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "schedule_type",
          "type": "VARCHAR(20)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "schedule_config",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "timezone",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "recipients",
          "type": "JSON",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "subject_template",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "message_template",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "last_run",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "next_run",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "report_type_id"
          ],
          "references": "report_types.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_report_schedule_next_run",
          "columns": [
            "next_run",
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "idx_report_schedule_org",
          "columns": [
            "organization_id",
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "report_types": {
      "category": "Analytics",
      "columns": [
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_parameters",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "data_retention_days",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "template_available",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_report_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_report_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "role_permissions": {
      "category": "User Management",
      "columns": [
        {
          "name": "role_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "permission_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 2,
          "autoincrement": false
        },
        {
          "name": "granted_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "role_id",
        "permission_id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "role_id"
          ],
          "references": "roles.['id']",
          "name": null
        },
        {
          "columns": [
            "permission_id"
          ],
          "references": "permissions.['id']",
          "name": null
        }
      ],
      "indexes": [],
      "row_count": 0
    },
    "roles": {
      "category": "User Management",
      "columns": [
        {
          "name": "name",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_system_role",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_default",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_role_default",
          "columns": [
            "is_default"
          ],
          "unique": 0
        },
        {
          "name": "idx_role_org_name",
          "columns": [
            "organization_id",
            "name"
          ],
          "unique": 0
        },
        {
          "name": "idx_role_system",
          "columns": [
            "is_system_role"
          ],
          "unique": 0
        },
        {
          "name": "ix_roles_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_roles_name",
          "columns": [
            "name"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "security_event_types": {
      "category": "Lookup Tables",
      "columns": [
        {
          "name": "severity",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_notification",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "log_level",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_security_event_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_security_event_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "security_events": {
      "category": "System",
      "columns": [
        {
          "name": "user_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "event_type_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "ip_address",
          "type": "VARCHAR(45)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "user_agent",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "user_id"
          ],
          "references": "users.['id']",
          "name": null
        },
        {
          "columns": [
            "event_type_id"
          ],
          "references": "security_event_types.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "ix_security_events_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "staff": {
      "category": "System",
      "columns": [
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "user_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "staff_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "staff_number",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "job_title",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "department",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "specialization",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "license_number",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "license_expiry",
          "type": "DATE",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "hire_date",
          "type": "DATE",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "termination_date",
          "type": "DATE",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "salary",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "employment_type",
          "type": "VARCHAR(20)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "work_email",
          "type": "VARCHAR(120)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "work_phone",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "emergency_contact_name",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "emergency_contact_phone",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "emergency_contact_relationship",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "office_location",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "office_hours",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "qualifications",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "certifications",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "languages_spoken",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "user_id"
          ],
          "references": "users.['id']",
          "name": null
        },
        {
          "columns": [
            "staff_id"
          ],
          "references": "staff.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_staff_hire_date",
          "columns": [
            "hire_date"
          ],
          "unique": 0
        },
        {
          "name": "idx_staff_job_title",
          "columns": [
            "job_title"
          ],
          "unique": 0
        },
        {
          "name": "idx_staff_org_number",
          "columns": [
            "organization_id",
            "staff_number"
          ],
          "unique": 0
        },
        {
          "name": "idx_staff_status",
          "columns": [
            "status"
          ],
          "unique": 0
        },
        {
          "name": "ix_staff_staff_number",
          "columns": [
            "staff_number"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "subscription_plans": {
      "category": "System",
      "columns": [
        {
          "name": "price_monthly",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "price_yearly",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_users",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_patients",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "features",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_subscription_plans_code",
          "columns": [
            "code"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "subscriptions": {
      "category": "System",
      "columns": [
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "plan_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "price",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "start_date",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "end_date",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "stripe_subscription_id",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "plan_id"
          ],
          "references": "subscription_plans.['id']",
          "name": null
        }
      ],
      "indexes": [],
      "row_count": 0
    },
    "suppliers": {
      "category": "Inventory",
      "columns": [
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "contact_name",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "contact_email",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "contact_phone",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "address",
          "type": "VARCHAR(255)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "city",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "state",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "postal_code",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "country",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "tax_id",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "payment_terms",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "lead_time_days",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "rating",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_preferred",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "website",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "notes",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "categories_served",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_supplier_org_name",
          "columns": [
            "organization_id",
            "name"
          ],
          "unique": 0
        },
        {
          "name": "idx_supplier_preferred",
          "columns": [
            "is_preferred"
          ],
          "unique": 0
        },
        {
          "name": "idx_supplier_status",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_suppliers_name",
          "columns": [
            "name"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "tenant_audit_logs": {
      "category": "System",
      "columns": [
        {
          "name": "tenant_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "user_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "action",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "resource_type",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "resource_id",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "details",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "ip_address",
          "type": "VARCHAR(45)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "user_agent",
          "type": "VARCHAR(500)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "tenant_id"
          ],
          "references": "tenants.['id']",
          "name": null
        },
        {
          "columns": [
            "user_id"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "ix_tenant_audit_logs_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "tenant_invitations": {
      "category": "System",
      "columns": [
        {
          "name": "tenant_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "email",
          "type": "VARCHAR(120)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "role",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "token",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "invited_by",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "expires_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "accepted_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "tenant_id"
          ],
          "references": "tenants.['id']",
          "name": null
        },
        {
          "columns": [
            "invited_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "ix_tenant_invitations_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_tenant_invitations_token",
          "columns": [
            "token"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "tenant_statuses": {
      "category": "Lookup Tables",
      "columns": [
        {
          "name": "allows_login",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_action",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_trial_status",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_tenant_statuses_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_tenant_statuses_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "tenants": {
      "category": "System",
      "columns": [
        {
          "name": "name",
          "type": "VARCHAR(200)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "subdomain",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "display_name",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "industry_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "contact_email",
          "type": "VARCHAR(120)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "contact_phone",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "website",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "address_line1",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "address_line2",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "city",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "state",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "postal_code",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "country",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "timezone",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "subscription_plan_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "stripe_customer_id",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "stripe_subscription_id",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "trial_ends_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "subscription_ends_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "billing_cycle_start",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "billing_cycle_end",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_users",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_patients",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_storage_mb",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "features_enabled",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "logo_url",
          "type": "VARCHAR(500)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "favicon_url",
          "type": "VARCHAR(500)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "theme_settings",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "custom_domain",
          "type": "VARCHAR(200)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "settings",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "business_hours",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "holiday_schedule",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "privacy_policy_url",
          "type": "VARCHAR(500)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "terms_of_service_url",
          "type": "VARCHAR(500)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "data_retention_days",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "compliance_settings",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "activated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "activated_by",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "industry_id"
          ],
          "references": "industry_types.['id']",
          "name": null
        },
        {
          "columns": [
            "subscription_plan_id"
          ],
          "references": "subscription_plans.['id']",
          "name": null
        },
        {
          "columns": [
            "status_id"
          ],
          "references": "tenant_statuses.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_tenant_contact_email",
          "columns": [
            "contact_email"
          ],
          "unique": 0
        },
        {
          "name": "idx_tenant_created_at",
          "columns": [
            "created_at"
          ],
          "unique": 0
        },
        {
          "name": "idx_tenant_custom_domain",
          "columns": [
            "custom_domain"
          ],
          "unique": 0
        },
        {
          "name": "idx_tenant_status_plan",
          "columns": [
            "status_id",
            "subscription_plan_id"
          ],
          "unique": 0
        },
        {
          "name": "ix_tenants_contact_email",
          "columns": [
            "contact_email"
          ],
          "unique": 0
        },
        {
          "name": "ix_tenants_custom_domain",
          "columns": [
            "custom_domain"
          ],
          "unique": 1
        },
        {
          "name": "ix_tenants_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_tenants_name",
          "columns": [
            "name"
          ],
          "unique": 1
        },
        {
          "name": "ix_tenants_stripe_customer_id",
          "columns": [
            "stripe_customer_id"
          ],
          "unique": 0
        },
        {
          "name": "ix_tenants_subdomain",
          "columns": [
            "subdomain"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "treatment_priorities": {
      "category": "Clinical Data",
      "columns": [
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_treatment_priorities_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_treatment_priorities_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 4
    },
    "treatment_rooms": {
      "category": "Clinical Data",
      "columns": [
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "room_number",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "room_type",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "equipment",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "ix_treatment_rooms_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "treatment_statuses": {
      "category": "Clinical Data",
      "columns": [
        {
          "name": "allows_modification",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_completed_status",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_treatment_statuses_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_treatment_statuses_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 5
    },
    "treatment_types": {
      "category": "Clinical Data",
      "columns": [
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "complexity_level",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "typical_duration",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_treatment_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_treatment_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 10
    },
    "treatments": {
      "category": "Clinical Data",
      "columns": [
        {
          "name": "tenant_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "patient_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "dentist_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "assistant_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "treatment_type_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "status_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "priority_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(200)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "procedure_code",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "diagnosis_codes",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "scheduled_date",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "estimated_duration",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "actual_start_time",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "actual_end_time",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "actual_duration",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "tooth_numbers",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "surfaces",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "anesthesia_used",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "complications",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "post_treatment_instructions",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "cost_estimate",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "actual_cost",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "insurance_covered",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "patient_responsibility",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "duration",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "price",
          "type": "NUMERIC(10, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "tenant_id"
          ],
          "references": "tenants.['id']",
          "name": null
        },
        {
          "columns": [
            "patient_id"
          ],
          "references": "patients.['id']",
          "name": null
        },
        {
          "columns": [
            "dentist_id"
          ],
          "references": "users.['id']",
          "name": null
        },
        {
          "columns": [
            "assistant_id"
          ],
          "references": "users.['id']",
          "name": null
        },
        {
          "columns": [
            "treatment_type_id"
          ],
          "references": "treatment_types.['id']",
          "name": null
        },
        {
          "columns": [
            "status_id"
          ],
          "references": "treatment_statuses.['id']",
          "name": null
        },
        {
          "columns": [
            "priority_id"
          ],
          "references": "treatment_priorities.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_treatment_dentist_date",
          "columns": [
            "dentist_id",
            "scheduled_date"
          ],
          "unique": 0
        },
        {
          "name": "idx_treatment_patient_status",
          "columns": [
            "patient_id",
            "status_id"
          ],
          "unique": 0
        },
        {
          "name": "idx_treatment_procedure_code",
          "columns": [
            "procedure_code"
          ],
          "unique": 0
        },
        {
          "name": "idx_treatment_type",
          "columns": [
            "treatment_type_id"
          ],
          "unique": 0
        },
        {
          "name": "ix_treatments_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_treatments_procedure_code",
          "columns": [
            "procedure_code"
          ],
          "unique": 0
        },
        {
          "name": "ix_treatments_scheduled_date",
          "columns": [
            "scheduled_date"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "user_oauths": {
      "category": "User Management",
      "columns": [
        {
          "name": "user_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "provider",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "provider_user_id",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "access_token",
          "type": "VARCHAR(255)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "refresh_token",
          "type": "VARCHAR(255)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "token_expiry",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "user_id"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "ix_user_oauths_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "user_roles": {
      "category": "User Management",
      "columns": [
        {
          "name": "is_system_role",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "access_level",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "can_manage_users",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "can_access_reports",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_user_roles_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_user_roles_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "user_roles_association": {
      "category": "User Management",
      "columns": [
        {
          "name": "user_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "role_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 2,
          "autoincrement": false
        },
        {
          "name": "assigned_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "user_id",
        "role_id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "user_id"
          ],
          "references": "users.['id']",
          "name": null
        },
        {
          "columns": [
            "role_id"
          ],
          "references": "roles.['id']",
          "name": null
        }
      ],
      "indexes": [],
      "row_count": 0
    },
    "user_sessions": {
      "category": "User Management",
      "columns": [
        {
          "name": "user_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "session_token",
          "type": "VARCHAR(255)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "ip_address",
          "type": "VARCHAR(45)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "user_agent",
          "type": "VARCHAR(255)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "login_time",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "logout_time",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "user_id"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [],
      "row_count": 0
    },
    "users": {
      "category": "User Management",
      "columns": [
        {
          "name": "email",
          "type": "VARCHAR(120)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "password_hash",
          "type": "VARCHAR(128)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "first_name",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "last_name",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "phone",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "avatar_url",
          "type": "VARCHAR(255)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "bio",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "date_of_birth",
          "type": "DATE",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "gender_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "specialization",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "license_number",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "experience_years",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "clinic_name",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "user_role_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "custom_role_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "tenant_id",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_admin",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "last_login",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "last_activity",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "stripe_customer_id",
          "type": "VARCHAR(255)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "settings",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "gender_id"
          ],
          "references": "genders.['id']",
          "name": null
        },
        {
          "columns": [
            "user_role_id"
          ],
          "references": "user_roles.['id']",
          "name": null
        },
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "custom_role_id"
          ],
          "references": "roles.['id']",
          "name": null
        },
        {
          "columns": [
            "tenant_id"
          ],
          "references": "tenants.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_user_activity",
          "columns": [
            "last_activity"
          ],
          "unique": 0
        },
        {
          "name": "idx_user_email_org",
          "columns": [
            "email",
            "organization_id"
          ],
          "unique": 0
        },
        {
          "name": "idx_user_last_login",
          "columns": [
            "last_login"
          ],
          "unique": 0
        },
        {
          "name": "idx_user_role_status",
          "columns": [
            "user_role_id",
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "idx_user_tenant",
          "columns": [
            "tenant_id"
          ],
          "unique": 0
        },
        {
          "name": "ix_users_email",
          "columns": [
            "email"
          ],
          "unique": 1
        },
        {
          "name": "ix_users_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "vital_signs": {
      "category": "System",
      "columns": [
        {
          "name": "patient_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "recorded_by",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "blood_pressure_systolic",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "blood_pressure_diastolic",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "heart_rate",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "respiratory_rate",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "temperature",
          "type": "NUMERIC(4, 1)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "oxygen_saturation",
          "type": "NUMERIC(4, 1)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "height",
          "type": "NUMERIC(4, 1)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "weight",
          "type": "NUMERIC(5, 2)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "bmi",
          "type": "NUMERIC(4, 1)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "record_date",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "notes",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "position",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "patient_id"
          ],
          "references": "patients.['id']",
          "name": null
        },
        {
          "columns": [
            "recorded_by"
          ],
          "references": "users.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_vital_sign_date",
          "columns": [
            "record_date"
          ],
          "unique": 0
        },
        {
          "name": "idx_vital_sign_patient_date",
          "columns": [
            "patient_id",
            "record_date"
          ],
          "unique": 0
        },
        {
          "name": "ix_vital_signs_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "vital_signs_units": {
      "category": "System",
      "columns": [
        {
          "name": "unit_type",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "conversion_factor",
          "type": "FLOAT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "si_unit",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_vital_signs_units_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_vital_signs_units_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 5
    },
    "webhook_event_statuses": {
      "category": "Lookup Tables",
      "columns": [
        {
          "name": "is_final_status",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "allows_retry",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_retries",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_webhook_event_statuses_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_webhook_event_statuses_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "widget_templates": {
      "category": "System",
      "columns": [
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "title",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "widget_type_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "default_config",
          "type": "JSON",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "default_size",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_system_template",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "required_permission",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "widget_type_id"
          ],
          "references": "widget_types.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_widget_template_category",
          "columns": [
            "category"
          ],
          "unique": 0
        },
        {
          "name": "idx_widget_template_system",
          "columns": [
            "is_system_template"
          ],
          "unique": 0
        },
        {
          "name": "ix_widget_templates_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        },
        {
          "name": "ix_widget_templates_name",
          "columns": [
            "name"
          ],
          "unique": 1
        }
      ],
      "row_count": 0
    },
    "widget_types": {
      "category": "Lookup Tables",
      "columns": [
        {
          "name": "default_size",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "category",
          "type": "VARCHAR(50)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "supports_refresh",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "max_data_points",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "code",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "name",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "sort_order",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "color",
          "type": "VARCHAR(7)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_widget_types_code",
          "columns": [
            "code"
          ],
          "unique": 1
        },
        {
          "name": "ix_widget_types_is_active",
          "columns": [
            "is_active"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    },
    "widgets": {
      "category": "System",
      "columns": [
        {
          "name": "user_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "organization_id",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "widget_type_id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "title",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "description",
          "type": "TEXT",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "size",
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "position_x",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "position_y",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "width",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "height",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "config",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "data_source",
          "type": "JSON",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "refresh_interval",
          "type": "INTEGER",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "filters",
          "type": "JSON",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_visible",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "requires_permission",
          "type": "VARCHAR(100)",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "primary_key": 1,
          "autoincrement": false
        },
        {
          "name": "public_id",
          "type": "VARCHAR(36)",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "nullable": false,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "nullable": true,
          "default": "None",
          "primary_key": 0,
          "autoincrement": false
        }
      ],
      "primary_keys": [
        "id"
      ],
      "foreign_keys": [
        {
          "columns": [
            "user_id"
          ],
          "references": "users.['id']",
          "name": null
        },
        {
          "columns": [
            "organization_id"
          ],
          "references": "organizations.['public_id']",
          "name": null
        },
        {
          "columns": [
            "widget_type_id"
          ],
          "references": "widget_types.['id']",
          "name": null
        }
      ],
      "indexes": [
        {
          "name": "idx_widget_user_org",
          "columns": [
            "user_id",
            "organization_id"
          ],
          "unique": 0
        }
      ],
      "row_count": 0
    }
  },
  "statistics": {
    "total_tables": 77,
    "table_categories": {
      "System": 26,
      "Analytics": 8,
      "Appointments": 2,
      "Financial": 4,
      "Lookup Tables": 9,
      "Inventory": 13,
      "Clinical Data": 6,
      "User Management": 9
    }
  }
};

document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    const navLinks = document.querySelectorAll('.nav-link');
    const contentTitle = document.getElementById('content-title');
    const tableDetails = document.getElementById('table-details');
    const systemOverview = document.getElementById('system-overview');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const tableName = this.getAttribute('data-table');
            showTableDetails(tableName);
        });
    });
    
    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', function() {
        location.reload();
    });
    
    // Export button
    document.getElementById('export-btn').addEventListener('click', function() {
        exportData();
    });
    
    function showTableDetails(tableName) {
        const tableInfo = schemaInfo.tables[tableName];
        if (!tableInfo) return;
        
        // Update UI
        contentTitle.textContent = `📊 ${tableName}`;
        systemOverview.classList.remove('active');
        tableDetails.classList.add('active');
        tableDetails.innerHTML = generateTableHTML(tableName, tableInfo);
        
        // Load sample data
        loadSampleData(tableName);
    }
    
    function generateTableHTML(tableName, tableInfo) {
        return `
            <div class="table-container">
                <div class="table-header">
                    <h3>Table Structure: ${tableName}</h3>
                    <div class="table-stats">
                        <span>${tableInfo.columns.length} columns • ${tableInfo.row_count} rows</span>
                    </div>
                </div>
                <div class="table-content">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Column Name</th>
                                <th>Data Type</th>
                                <th>Properties</th>
                                <th>Default</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${tableInfo.columns.map(column => `
                                <tr>
                                    <td><strong>${column.name}</strong></td>
                                    <td><span class="column-type">${column.type}</span></td>
                                    <td>
                                        <div class="column-props">
                                            ${column.primary_key ? '<span class="prop-tag prop-pk">PK</span>' : ''}
                                            ${column.autoincrement ? '<span class="prop-tag prop-pk">AI</span>' : ''}
                                            ${column.nullable ? '<span class="prop-tag prop-nullable">NULL</span>' : '<span class="prop-tag">NOT NULL</span>'}
                                            ${tableInfo.foreign_keys.some(fk => fk.columns.includes(column.name)) ? '<span class="prop-tag prop-fk">FK</span>' : ''}
                                            ${tableInfo.indexes.some(idx => idx.unique && idx.columns.includes(column.name)) ? '<span class="prop-tag prop-unique">UNIQUE</span>' : ''}
                                        </div>
                                    </td>
                                    <td>${column.default || '-'}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div style="margin-top: 20px;">
                <h4>Sample Data</h4>
                <div id="sample-data-${tableName}">
                    <p>Loading sample data...</p>
                </div>
            </div>
        `;
    }
    
    async function loadSampleData(tableName) {
        try {
            const response = await fetch(`/admin-api/data/${tableName}?limit=10`);
            const data = await response.json();
            displaySampleData(tableName, data);
        } catch (error) {
            document.getElementById(`sample-data-${tableName}`).innerHTML = 
                '<p>Error loading sample data</p>';
        }
    }
    
    function displaySampleData(tableName, data) {
        const container = document.getElementById(`sample-data-${tableName}`);
        if (!data || data.length === 0) {
            container.innerHTML = '<p>No data found</p>';
            return;
        }
        
        const headers = Object.keys(data[0]);
        const html = `
            <div class="table-container">
                <div class="table-content">
                    <table class="data-table">
                        <thead>
                            <tr>
                                ${headers.map(header => `<th>${header}</th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            ${data.map(row => `
                                <tr>
                                    ${headers.map(header => `<td>${formatCellValue(row[header])}</td>`).join('')}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    function formatCellValue(value) {
        if (value === null || value === undefined) return '<em>null</em>';
        if (typeof value === 'boolean') return value ? '✅' : '❌';
        if (typeof value === 'object') return JSON.stringify(value).substring(0, 50) + '...';
        return String(value);
    }
    
    function exportData() {
        // Simple export functionality
        const dataStr = JSON.stringify(schemaInfo, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'dentaloist-schema-export.json';
        link.click();
        URL.revokeObjectURL(url);
    }
});
