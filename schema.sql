-- Tickets table simulating GLPI incidents and assets
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    department TEXT NOT NULL,
    equipment_type TEXT NOT NULL,
    asset_tag TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    root_cause TEXT,
    solution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table for login role routing
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('staff', 'tech', 'admin')),
    department TEXT
);