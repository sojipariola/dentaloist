-- Row Level Security (PostgreSQL example)
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON patients
    USING (organization_id = current_setting('app.current_tenant_id'));

-- Function to set tenant context
CREATE OR REPLACE FUNCTION set_tenant_context(tenant_id TEXT)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.current_tenant_id', tenant_id, false);
END;
$$ LANGUAGE plpgsql;