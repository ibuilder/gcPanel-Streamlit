-- Highland Tower Development Construction Management Database Schema
-- PostgreSQL Database Schema for gcPanel Application

-- Users and Authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Projects
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15, 2),
    status VARCHAR(50) DEFAULT 'active',
    project_manager_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Daily Reports
CREATE TABLE IF NOT EXISTS daily_reports (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    report_date DATE NOT NULL,
    weather VARCHAR(50),
    temperature INTEGER,
    wind VARCHAR(50),
    crew_size INTEGER,
    work_performed TEXT,
    issues_delays TEXT,
    tomorrow_plan TEXT,
    safety_incidents INTEGER DEFAULT 0,
    inspections TEXT,
    materials_delivered TEXT,
    created_by INTEGER REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- RFIs (Request for Information)
CREATE TABLE IF NOT EXISTS rfis (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    rfi_number VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    drawing_reference VARCHAR(255),
    specification_section VARCHAR(255),
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(50) DEFAULT 'open',
    date_submitted DATE DEFAULT CURRENT_DATE,
    date_required DATE,
    date_answered DATE,
    submitted_by INTEGER REFERENCES users(id),
    assigned_to INTEGER REFERENCES users(id),
    response TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Submittals
CREATE TABLE IF NOT EXISTS submittals (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    submittal_number VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    specification_section VARCHAR(255),
    submittal_type VARCHAR(50),
    status VARCHAR(50) DEFAULT 'pending',
    date_submitted DATE DEFAULT CURRENT_DATE,
    date_required DATE,
    date_reviewed DATE,
    submitted_by INTEGER REFERENCES users(id),
    reviewed_by INTEGER REFERENCES users(id),
    review_comments TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Safety Incidents
CREATE TABLE IF NOT EXISTS safety_incidents (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    incident_date DATE NOT NULL,
    incident_time TIME,
    location VARCHAR(255),
    incident_type VARCHAR(100),
    severity VARCHAR(50),
    description TEXT,
    injured_person VARCHAR(255),
    witness VARCHAR(255),
    immediate_action TEXT,
    root_cause TEXT,
    corrective_action TEXT,
    reported_by INTEGER REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Contracts
CREATE TABLE IF NOT EXISTS contracts (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    contract_number VARCHAR(50) UNIQUE NOT NULL,
    contractor_name VARCHAR(255) NOT NULL,
    contract_type VARCHAR(50),
    contract_value DECIMAL(15, 2),
    start_date DATE,
    end_date DATE,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Change Orders
CREATE TABLE IF NOT EXISTS change_orders (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER REFERENCES contracts(id),
    change_order_number VARCHAR(50) NOT NULL,
    description TEXT,
    reason TEXT,
    cost_impact DECIMAL(15, 2),
    time_impact INTEGER, -- days
    status VARCHAR(50) DEFAULT 'pending',
    date_submitted DATE DEFAULT CURRENT_DATE,
    date_approved DATE,
    approved_by INTEGER REFERENCES users(id),
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Inspections
CREATE TABLE IF NOT EXISTS inspections (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    inspection_type VARCHAR(100) NOT NULL,
    inspection_date DATE NOT NULL,
    inspector_name VARCHAR(255),
    location VARCHAR(255),
    status VARCHAR(50) DEFAULT 'scheduled',
    result VARCHAR(50),
    deficiencies TEXT,
    corrective_actions TEXT,
    next_inspection_date DATE,
    conducted_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Documents
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    document_type VARCHAR(50),
    file_path VARCHAR(500),
    file_name VARCHAR(255),
    file_size INTEGER,
    mime_type VARCHAR(100),
    version VARCHAR(20) DEFAULT '1.0',
    status VARCHAR(50) DEFAULT 'active',
    uploaded_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Cost Tracking
CREATE TABLE IF NOT EXISTS cost_items (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    category VARCHAR(100),
    item_description TEXT,
    budgeted_amount DECIMAL(15, 2),
    actual_amount DECIMAL(15, 2) DEFAULT 0,
    variance DECIMAL(15, 2) GENERATED ALWAYS AS (actual_amount - budgeted_amount) STORED,
    date_incurred DATE,
    status VARCHAR(50) DEFAULT 'active',
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Material Management
CREATE TABLE IF NOT EXISTS materials (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    material_name VARCHAR(255) NOT NULL,
    description TEXT,
    unit VARCHAR(50),
    quantity_ordered DECIMAL(10, 2),
    quantity_received DECIMAL(10, 2) DEFAULT 0,
    quantity_used DECIMAL(10, 2) DEFAULT 0,
    unit_cost DECIMAL(10, 2),
    supplier VARCHAR(255),
    delivery_date DATE,
    status VARCHAR(50) DEFAULT 'ordered',
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Equipment Tracking
CREATE TABLE IF NOT EXISTS equipment (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    equipment_name VARCHAR(255) NOT NULL,
    equipment_type VARCHAR(100),
    serial_number VARCHAR(100),
    location VARCHAR(255),
    status VARCHAR(50) DEFAULT 'available',
    rental_rate DECIMAL(10, 2),
    maintenance_date DATE,
    next_maintenance_date DATE,
    assigned_to INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Progress Photos
CREATE TABLE IF NOT EXISTS progress_photos (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    title VARCHAR(255),
    description TEXT,
    photo_date DATE DEFAULT CURRENT_DATE,
    location VARCHAR(255),
    file_path VARCHAR(500),
    file_name VARCHAR(255),
    file_size INTEGER,
    weather_conditions VARCHAR(100),
    photographer INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert default Highland Tower project
INSERT INTO projects (id, name, description, location, start_date, end_date, budget, status) 
VALUES (1, 'Highland Tower Development', 'Mixed-use development with residential and commercial spaces', 
        'Downtown Highland District', '2024-01-15', '2026-03-30', 45500000.00, 'active')
ON CONFLICT (id) DO NOTHING;

-- Insert default admin user
INSERT INTO users (id, username, password_hash, email, first_name, last_name, role) 
VALUES (1, 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 
        'admin@highland-tower.com', 'Admin', 'User', 'admin')
ON CONFLICT (username) DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_daily_reports_date ON daily_reports(report_date);
CREATE INDEX IF NOT EXISTS idx_daily_reports_project ON daily_reports(project_id);
CREATE INDEX IF NOT EXISTS idx_rfis_project ON rfis(project_id);
CREATE INDEX IF NOT EXISTS idx_rfis_status ON rfis(status);
CREATE INDEX IF NOT EXISTS idx_submittals_project ON submittals(project_id);
CREATE INDEX IF NOT EXISTS idx_submittals_status ON submittals(status);
CREATE INDEX IF NOT EXISTS idx_documents_project ON documents(project_id);
CREATE INDEX IF NOT EXISTS idx_safety_incidents_project ON safety_incidents(project_id);
CREATE INDEX IF NOT EXISTS idx_contracts_project ON contracts(project_id);