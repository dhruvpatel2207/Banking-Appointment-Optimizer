CREATE DATABASE healthcare;

USE healthcare;

-- Patients table
CREATE TABLE Patients (
    Patient_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Age INT,
    Gender VARCHAR(10),
    Blood_Type VARCHAR(5)
);

-- Medical Conditions table
CREATE TABLE MedicalConditions (
    Condition_ID INT AUTO_INCREMENT PRIMARY KEY,
    Patient_ID INT NOT NULL,
    Medical_Condition VARCHAR(255),
    Admission_Type VARCHAR(50),
    Medication VARCHAR(255),
    Test_Results TEXT,
    FOREIGN KEY (Patient_ID) REFERENCES Patients(Patient_ID)
);

-- Admissions table
CREATE TABLE Admissions (
    Admission_ID INT AUTO_INCREMENT PRIMARY KEY,
    Patient_ID INT NOT NULL,
    Admission_Date DATE,
    Discharge_Date DATE,
    Scheduled_Date DATE,
    Hospital VARCHAR(255),
    Billing_Amount DECIMAL(10, 2),
    FOREIGN KEY (Patient_ID) REFERENCES Patients(Patient_ID)
);
