# Subsystem C: IoT Device, Communication & Notifications

## 1. Diagrams Chosen
- Use Case Diagram – Device Pairings & Alerts
- Sequence Diagram – Device Onboarding & Calibration
- Activity Diagram – IoT Device Firmware Runtime

## 2. Mermaid Diagrams

### 2.1 Use Case Diagram – Device Pairings & Alerts
```mermaid
graph TD
    %% Actors with STEREOTYPE notation
    A1["Pet Owner\n&lt;&lt;Actor&gt;&gt;"]
    A2["IoT Feeder\n&lt;&lt;Actor&gt;&gt;"]
    A3["Notification Service\n&lt;&lt;Actor&gt;&gt;"]

    %% Boundaries
    subgraph IoT_Notification ["Subsystem C: IoT Device, Communication & Notifications"]
        UC1(("Pair Device (S/N + Code)"))
        UC2(("Calibrate HX711 Sensors"))
        UC3(("Report Sensor Data"))
        UC4(("Configure Alerts"))
        UC5(("Receive Low Food/Water Alert"))
        UC6(("Receive Online/Offline Alert"))
        UC7(("Unpair Device"))
    end

    %% Relationships
    A1 --- UC1
    A1 --- UC2
    A1 --- UC4
    A1 --- UC5
    A1 --- UC6
    A1 --- UC7

    A2 --- UC3
    A2 --- UC1

    UC1 -.->|&lt;&lt;include&gt;&gt;| UC6
    UC5 --- A3
    UC6 --- A3
    UC3 -.->|&lt;&lt;trigger&gt;&gt;| UC5

    %% Styling
    classDef actor fill:#f5f5f5,stroke:#333,stroke-width:2px;
    classDef usecase fill:#ffffff,stroke:#333,stroke-width:1px;
    class A1,A2,A3 actor
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7 usecase
```

### 2.2 Sequence Diagram – Device Onboarding & Calibration
```mermaid
sequenceDiagram
    autonumber
    actor User as Pet Owner
    participant App as Mobile/Web App
    participant BE as Backend Server
    participant ESP32 as IoT Feeder (ESP32)
    participant DB as System Database

    User->>App: Enter S/N & Pairing Code
    activate App
    App->>BE: POST /devices/pair {sn, code}
    activate BE
    BE->>DB: Verify S/N and Hash(Code)
    activate DB
    DB-->>BE: Match Found & Available
    deactivate DB
    BE->>DB: Assign owner_id = current_user
    activate DB
    DB-->>BE: Update Success
    deactivate DB
    BE-->>App: Pairing Successful
    deactivate BE
    App-->>User: Show Dashboard
    deactivate App
    
    User->>App: Start Calibration
    activate App
    App->>BE: PUT /devices/{id}/calibrate
    activate BE
    BE->>ESP32: Queue CALIBRATE command
    deactivate BE
    deactivate App
    
    activate ESP32
    Note over ESP32: Wait for empty hopper
    ESP32->>ESP32: Zero Tare HX711
    ESP32-->>BE: Calibration Data Reported
    activate BE
    BE->>DB: Update calibration_data
    activate DB
    DB-->>BE: Save Success
    deactivate DB
    deactivate BE
    deactivate ESP32
```

### 2.3 Activity Diagram – IoT Device Firmware Runtime
```mermaid
stateDiagram-v2
    state "ESP32 Boot" as S1 {
        direction TB
        [*] --> PowerOn
        PowerOn --> ConnectWiFi
        ConnectWiFi --> RegisterSession
    }

    state "Runtime Loop" as S2 {
        direction TB
        RegisterSession --> PollCommands
        PollCommands --> ExecuteLogic: If command found
        ExecuteLogic --> UpdateCommandState
        UpdateCommandState --> ReadSensors
    }

    state "Cloud Reporting" as S3 {
        direction TB
        ReadSensors --> ReportSensors
        ReportSensors --> CheckAnomalies
        CheckAnomalies --> Sleep
        Sleep --> PollCommands
    }
```

## 3. Documentation Draft Sections

### 6.1 Use Case Diagram – Device Pairing & Notification Subsystem
**Purpose:**
This diagram maps the initial setup of hardware and the subsequent automated alerting mechanisms that keep the user informed.

**Subsystem Representation:**
Represents the "IoT Device, Communication & Notifications" subsystem, encompassing hardware interaction and external notification triggers.

**Explanation of Key Elements:**
- **Notification Service Actor:** A stereotyped external service that bridges system events to the user.
- **Sensor-Triggered Alerts:** Illustrates the automated flow where sensor data reports lead directly to user notifications.

**System Design Decisions:**
The choice to require a physical "Pairing Code" alongside a Serial Number provides a primitive but effective form of multi-factor authentication for hardware deployment.

---

### 6.2 Sequence Diagram – Device Onboarding Subsystem
**Purpose:**
To detail the handshake process between the frontend, backend, and hardware during initial deployment, utilizing activation bars to denote processing scope.

**Subsystem Representation:**
Details the "Connectivity & Setup" module.

**Explanation of Key Elements:**
- **Code Hashing:** Security measure where pairing codes are never stored in plain text.
- **Calibration Loop:** Shows how sensor accuracy is established at the hardware level but stored at the cloud level.

**System Design Decisions:**
Decoupling the pairing result from the calibration process allows the user to immediately access the dashboard while hardware-specific tuning happens as a background task.

---

### 6.3 Activity Diagram – IoT Device Runtime Subsystem
**Purpose:**
To model the continuous logic loop of the ESP32 firmware using swimlanes to separate boot logic, local processing, and cloud reporting.

**Subsystem Representation:**
Represents the Firmware and Communication protocol of the hardware.

**Explanation of Key Elements:**
- **Poll-Execute-Report Pattern:** The fundamental operating cycle for the device.
- **Anomaly Detection:** Internal firmware check that proactively reports issues before being polled.

**System Design Decisions:**
The decision to utilize a polling interval (10-30s) instead of active persistent connections reduces server overhead and allows the device to function effectively behind consumer firewalls.
