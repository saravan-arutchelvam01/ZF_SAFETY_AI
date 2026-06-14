CREATE DATABASE IF NOT EXISTS zf_safety_ai;

USE zf_safety_ai;

CREATE TABLE production_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    component_type VARCHAR(50),
    machine_id VARCHAR(20),

    temperature FLOAT,
    vibration FLOAT,
    pressure FLOAT,
    motor_current FLOAT,

    production_speed FLOAT,
    defect_count INT,

    humidity FLOAT,
    torque FLOAT,
    sensor_accuracy FLOAT,

    risk_level INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id VARCHAR(20),
    component_type VARCHAR(50),
    risk_level INT,
    alert_message VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);