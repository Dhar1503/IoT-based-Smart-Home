-- ===========================================
-- SMART HOME SECURITY & SURVEILLANCE DATABASE
-- ===========================================

-- Drop existing tables (optional)
DROP TABLE IF EXISTS Event;
DROP TABLE IF EXISTS Device;
DROP TABLE IF EXISTS User;

-- ====================
-- 1. USER TABLE
-- ====================
CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Insert default admin user
INSERT INTO User (username, password)
VALUES ('admin', 'admin123');

-- ====================
-- 2. DEVICE TABLE
-- ====================
CREATE TABLE Device (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    device_type TEXT NOT NULL,
    status TEXT NOT NULL
);

-- Insert initial IoT devices
INSERT INTO Device (name, device_type, status) VALUES
('Front Door Lock', 'lock', 'locked'),
('Living Room Camera', 'camera', 'online'),
('Motion Sensor', 'motion', 'active'),
('Gas Sensor', 'gas', 'active');

-- ====================
-- 3. EVENT TABLE
-- ====================
CREATE TABLE Event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_name TEXT NOT NULL,
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    temperature REAL,
    humidity REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert a few example events
INSERT INTO Event (device_name, event_type, message, temperature, humidity)
VALUES
('Living Room Sensor', 'info', 'Temperature 28°C, Humidity 50%', 28, 50),
('Kitchen Sensor', 'alert', 'Gas leakage detected!', NULL, NULL),
('Bedroom Sensor', 'info', 'Temperature 30°C, Humidity 45%', 30, 45);

