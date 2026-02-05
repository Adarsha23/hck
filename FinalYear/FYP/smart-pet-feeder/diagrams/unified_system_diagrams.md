# Unified System Diagrams

## 1. Diagrams Chosen
- Data Flow Diagram (DFD) – Level 0 & 1
- Entity Relationship Diagram (ERD) – Unified Model
- Class Diagram – Principal Architecture
- Connectivity Diagram – Hardware/Cloud Overview

## 2. Mermaid Diagrams

### 2.1 Data Flow Diagram (DFD) – Level 0 & 1
```mermaid
graph TD
    %% Level 0: Context Diagram
    subgraph DFD_Level_0 [System Context]
        E1["Pet Owner"]
        S[Smart Pet Feeder System]
        E2["IoT Device"]
        E3["Email Service"]
        
        E1 -- "Auth/Feed Trigger" --> S
        S -- "Notifications" --> E1
        S -- "Queued Commands" --> E2
        E2 -- "Sensor Readings" --> S
        S -- "Verification Link" --> E3
    end

    %% Level 1: Functional Decomposition
    subgraph DFD_Level_1 [Functional Flow]
        direction TB
        Process1["1.0 Identity Mgmt"]
        Process2["2.0 Dispensing Logic"]
        Process3["3.0 Analytics Engine"]
        Process4["4.0 IoT Sync Gateway"]
        
        DataStore1[("User/Pet DB")]
        DataStore2[("Event/Log DB")]
        DataStore3[("Command queue")]
        
        E1 -- "User Registration" --> Process1
        Process1 -- "Store Metadata" --> DataStore1
        
        E1 -- "Command (Gram)" --> Process2
        Process2 -- "Queue Command" --> DataStore3
        
        DataStore3 -- "Poll/Fetch" --> Process4
        Process4 -- "Relay to Device" --> E2
        E2 -- "Report Status" --> Process4
        Process4 -- "Persist Result" --> DataStore2
        
        DataStore2 -- "Retrieve Data" --> Process3
        Process3 -- "Visual Reports" --> E1
    end

    %% Styling
    classDef actor fill:#f5f5f5,stroke:#333,stroke-width:2px;
    classDef usecase fill:#ffffff,stroke:#333,stroke-width:1px;
    class E1,E2,E3 actor
    class Process1,Process2,Process3,Process4 usecase
```

### 2.2 Entity Relationship Diagram (ERD) – Unified Model
```mermaid
erDiagram
    USERS ||--o{ DEVICES : "owns"
    USERS ||--o{ PET_PROFILES : "manages"
    USERS ||--o{ NOTIFICATIONS : "receives"
    DEVICES ||--o{ FEEDING_EVENTS : "logs"
    DEVICES ||--o{ COMMAND_QUEUE : "receives"
    DEVICES ||--o{ DEVICE_SENSORS : "monitors"
    PET_PROFILES ||--o{ FEEDING_EVENTS : "associated_with"

    USERS {
        uuid id PK
        string email UK
        timestamp confirmed_at
    }
    DEVICES {
        uuid id PK
        string serial_number UK
        string status
        jsonb calibration_data
    }
    PET_PROFILES {
        uuid id PK
        uuid user_id FK
        string name
        decimal weight
    }
    COMMAND_QUEUE {
        uuid id PK
        uuid device_id FK
        string command_type
        jsonb payload
        string status
    }
    FEEDING_EVENTS {
        uuid id PK
        uuid device_id FK
        decimal actual_grams
        timestamp timestamp
    }
    DEVICE_SENSORS {
        uuid id PK
        uuid device_id FK
        string sensor_type
        decimal value
    }
```

### 2.3 Class Diagram – System Component Architecture
```mermaid
classDiagram
    direction TB
    
    %% Service Layer
    class AuthContext {
        -User user
        +signUp(email, password)
        +signIn(email, password)
    }
    class DeviceService {
        -SupabaseClient supabase
        +getUserDevices() Device[]
        +pairDevice(sn, code)
    }
    class FeedingService {
        -SupabaseClient supabase
        +getFeedingEvents() Event[]
        +triggerManualFeed(grams)
    }

    %% Data Models (DTOs)
    class User {
        +UUID id
        +string email
        +timestamp confirmed_at
    }
    class Device {
        +UUID id
        +string serial_number
        +DeviceStatus status
        +JSONB calibration_data
    }
    class PetProfile {
        +UUID id
        +string name
        +decimal weight
        +string photo_url
    }
    class FeedingEvent {
        +UUID id
        +decimal actual_grams
        +timestamp timestamp
    }

    %% Hardware Logic
    class ESP32Firmware {
        +HX711 loadCell
        +Servo motor
        +loop() 
        -pollCommandQueue()
        -executeDispense()
    }

    %% Relationships
    AuthContext -- User : manages
    DeviceService -- Device : retrieves
    FeedingService -- FeedingEvent : logs
    User "1" *-- "many" PetProfile : owns
    User "1" -- "many" Device : manages
    Device "1" -- "many" FeedingEvent : records
    ESP32Firmware ..> Device : hardware_for
```

### 2.4 Connectivity Diagram – Hardware-Rich Network Topology
```mermaid
graph TD
    subgraph IoT_Hardware [Smart Feeder Hardware]
        MCU["ESP32 Microcontroller"]
        
        subgraph Sensors [Monitoring]
            WC["HX711 Load Cell"]
            IR_F["Infrared (Food Level)"]
            IR_W["Infrared (Water Level)"]
        end
        
        subgraph Actuators [Dispensing]
            SV["Servo Motor"]
        end

        %% Local Connections
        MCU -- "Bit-bang (DT/SCK)" --> WC
        MCU -- "Digital I/O" --> IR_F
        MCU -- "Digital I/O" --> IR_W
        MCU -- "PWM Channel" --> SV
    end

    subgraph Service_Cloud [Supabase Cloud Stack]
        API["Backend API Layer"]
        DB[("PostgreSQL Database")]
        API --- DB
    end

    subgraph User_Interface [Frontend Layer]
        WEB["React Dashboard"]
    end

    %% Protocols
    MCU -- "HTTPS (REST)" --> API
    WEB -- "HTTPS / TLS" --> API
    WEB -- "JWT / WebSockets" --> API
```

## 3. Documentation Draft Sections

### 7.1 Data Flow Diagram (DFD)
**Purpose:**
To map the movement of information through the system, from user input to hardware execution and data persistence, without showing control flow.

**Subsystem Representation:**
Provides a cross-system view of data transitions across the management, execution, and analytics layers.

**Explanation of Key Elements:**
- **Level 1 (Functional Flow):** Explicitly separates the Identity management from the critical Dispensing logic and the IoT Sync Gateway.
- **Data Stores:** Identifies the central repositories for user metadata, command states, and operational logs.

**System Design Decisions:**
The architecture relies on a "Sync Gateway" process to handle the inherently unstable nature of IoT connectivity, ensuring that the core dispensing logic remains decoupled from the physical device's current online status.

---

### 7.2 Entity Relationship Diagram (ERD)
**Purpose:**
To model the database schema including primary/foreign keys and cardinalities, ensuring data integrity.

**Subsystem Representation:**
Represents the unified data model of the entire system.

**Explanation of Key Elements:**
- **Cardinalities:** Correctly maps that one user can own multiple devices but each device is owned by one user (1:N).
- **Entities:** Includes sensor logs and command queues as first-class citizens in the data model.

**System Design Decisions:**
Normalizing sensor data and feeding events into separate tables allows for high-frequency logs (sensors) to be purged or archived without affecting the historical feeding records.

---

### 7.3 Connectivity Diagram
**Purpose:**
To visualize the network and communication protocols used across the entire hardware-to-cloud ecosystem.

**Subsystem Representation:**
An architectural overview of the system connectivity.

**Explanation of Key Elements:**
- **Protocols (HTTPS, I2C, PWM):** Explicitly labels the communication standards used at each boundary.
- **Cloud Stack:** Details the internal components of the Supabase backend.

**System Design Decisions:**
The use of HTTPS/REST for the ESP32 is a deliberate choice to simplify firmware development and ensure compatibility with standard web proxies and firewalls.
