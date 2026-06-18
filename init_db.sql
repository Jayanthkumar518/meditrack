CREATE DATABASE IF NOT EXISTS stdmanagement;

USE stdmanagement;

CREATE TABLE equipment (
    equipment_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_name VARCHAR(100) NOT NULL,
    serial_number VARCHAR(50) UNIQUE NOT NULL,
    department VARCHAR(100),
    purchase_date DATE,
    status VARCHAR(50)
);

CREATE TABLE maintenance_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    maintenance_date DATE,
    technician_name VARCHAR(100),
    issue_reported TEXT,
    resolution_notes TEXT,
    next_due_date DATE,
    FOREIGN KEY (equipment_id)
    REFERENCES equipment(equipment_id)
    ON DELETE CASCADE
);