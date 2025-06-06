CREATE SCHEMA IF NOT EXISTS task_flow;

CREATE TABLE IF NOT EXISTS task_flow.custom_app_settings (
    id SERIAL PRIMARY KEY,
    environment VARCHAR(50) NOT NULL DEFAULT 'default',
    key VARCHAR(255) NOT NULL,
    value TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);