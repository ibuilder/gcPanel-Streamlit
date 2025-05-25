-- gcPanel Database Schema for Highland Tower Development
-- PostgreSQL Database Schema for Construction Management Platform

-- Users and Authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('admin', 'manager', 'engineer', 'supervisor', 'user')),
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Projects
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    contract_value DECIMAL(15,2),
    start_date DATE,
    planned_end_date DATE,
    actual_end_date DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('planning', 'active', 'on_hold', 'completed', 'cancelled')),
    project_manager_id INTEGER REFERENCES users(id),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Daily Reports
CREATE TABLE daily_reports (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    report_date DATE NOT NULL,
    weather_conditions VARCHAR(100),
    temperature_high INTEGER,
    temperature_low INTEGER,
    work_performed TEXT,
    delays_issues TEXT,
    safety_notes TEXT,
    crew_count INTEGER,
    equipment_on_site TEXT,
    materials_delivered TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RFIs (Request for Information)
CREATE TABLE rfis (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    rfi_number VARCHAR(50) UNIQUE NOT NULL,
    subject VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(100),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    submitted_by INTEGER REFERENCES users(id),
    assigned_to INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'pending', 'answered', 'closed')),
    due_date DATE,
    response_text TEXT,
    responded_by INTEGER REFERENCES users(id),
    responded_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Submittals
CREATE TABLE submittals (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    submittal_number VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    specification_section VARCHAR(50),
    contractor_name VARCHAR(100),
    description TEXT,
    submitted_by INTEGER REFERENCES users(id),
    reviewed_by INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'submitted' CHECK (status IN ('submitted', 'under_review', 'approved', 'rejected', 'resubmit_required')),
    priority VARCHAR(20) DEFAULT 'standard' CHECK (priority IN ('low', 'standard', 'high', 'critical')),
    due_date DATE,
    cost_impact DECIMAL(12,2) DEFAULT 0,
    schedule_impact VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_daily_reports_project_date ON daily_reports(project_id, report_date);
CREATE INDEX idx_rfis_project_status ON rfis(project_id, status);
CREATE INDEX idx_submittals_project_status ON submittals(project_id, status);

-- Insert Highland Tower Development project
INSERT INTO projects (name, description, contract_value, start_date, planned_end_date, status, address) 
VALUES (
    'Highland Tower Development',
    '$45.5M Mixed-Use Development - 120 Residential + 8 Retail Units - 15 Stories Above + 2 Below Ground',
    45500000.00,
    '2024-03-01',
    '2026-08-31',
    'active',
    'Highland District, Metropolitan Area'
);

-- Insert sample users
INSERT INTO users (username, email, password_hash, role, full_name, phone) VALUES
('admin', 'admin@highlandtower.com', '$2b$12$placeholder_hash', 'admin', 'System Administrator', '555-0001'),
('sarah.chen', 'sarah.chen@highlandtower.com', '$2b$12$placeholder_hash', 'engineer', 'Sarah Chen, PE', '555-0002'),
('mike.rodriguez', 'mike.rodriguez@highlandtower.com', '$2b$12$placeholder_hash', 'supervisor', 'Mike Rodriguez', '555-0003'),
('jennifer.walsh', 'jennifer.walsh@highlandtower.com', '$2b$12$placeholder_hash', 'manager', 'Jennifer Walsh, AIA', '555-0004'),
('david.kim', 'david.kim@highlandtower.com', '$2b$12$placeholder_hash', 'supervisor', 'David Kim', '555-0005');