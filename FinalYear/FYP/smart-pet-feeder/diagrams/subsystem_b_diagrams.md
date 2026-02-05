# Subsystem B: Feeding, Monitoring & Analytics

## 1. Diagrams Chosen
- Use Case Diagram – Feeding & Monitoring
- Sequence Diagram – Closed-Loop Feeding Operation
- Activity Diagram – Feeding Schedule & Execution Logic

## 2. Mermaid Diagrams

### 2.1 Use Case Diagram – Feeding & Monitoring
```mermaid
graph TD
    %% Actors with STEREOTYPE notation
    A1["Pet Owner\n&lt;&lt;Actor&gt;&gt;"]
    A2["Shared User\n&lt;&lt;Actor&gt;&gt;"]
    A3["IoT Feeder\n&lt;&lt;Actor&gt;&gt;"]

    %% Boundaries
    subgraph Feeding_Analytics ["Subsystem B: Feeding, Monitoring & Analytics"]
        UC1(("Manual Feeding"))
        UC2(("Schedule Feeding"))
        UC3(("Monitor Real-time Status"))
        UC4(("View Feeding History"))
        UC5(("View Analytics/Charts"))
        UC6(("Export Feeding Data"))
        UC7(("Cancel Pending Feed"))
        UC8(("Edit Schedule"))
    end

    %% Relationships
    A1 --- UC1
    A1 --- UC2
    A1 --- UC3
    A1 --- UC4
    A1 --- UC5
    A1 --- UC6
    A1 --- UC7
    A1 --- UC8

    A2 --- UC3
    A2 --- UC4
    A2 --- UC5

    A3 --- UC3
    
    UC1 -.->|&lt;&lt;extend&gt;&gt;| UC3
    UC2 -.->|&lt;&lt;include&gt;&gt;| UC4
    UC4 -.->|&lt;&lt;extend&gt;&gt;| UC6

    %% Styling
    classDef actor fill:#f5f5f5,stroke:#333,stroke-width:2px;
    classDef usecase fill:#ffffff,stroke:#333,stroke-width:1px;
    class A1,A2,A3 actor
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8 usecase
```

### 2.2 Sequence Diagram – Closed-Loop Feeding Operation
```mermaid
sequenceDiagram
    autonumber
    actor User as Pet Owner
    participant App as Mobile/Web App
    participant BE as Backend Server
    participant Queue as Command Queue
    participant ESP32 as IoT Feeder (ESP32)
    participant LC as Load Cell
    participant DB as Feeding History

    User->>App: Initiate Manual Feed (50g)
    activate App
    App->>BE: POST /feed {grams: 50}
    activate BE
    BE->>Queue: Push Command {type: FEED, target: 50}
    activate Queue
    Queue-->>BE: Command Queued
    deactivate Queue
    BE-->>App: Feedback: Command Pending
    deactivate BE
    deactivate App

    Note over ESP32: Wake/Poll Loop
    ESP32->>Queue: GET /polling?status=PENDING
    activate Queue
    Queue-->>ESP32: Send Command (50g)
    deactivate Queue
    
    activate ESP32
    loop Closed-Loop Control
        ESP32->>ESP32: Activate Servo (Dispensing)
        ESP32->>LC: Read Weight (HX711)
        LC-->>ESP32: Weight Data (grams)
        Note over ESP32: Is current_grams >= target?
    end
    ESP32->>ESP32: Stop Servo
    
    ESP32->>BE: POST /feeding-result {actual: 49.5, status: SUCCESS}
    activate BE
    BE->>DB: Record Event
    activate DB
    DB-->>BE: Record Success
    deactivate DB
    BE-->>App: Push Real-time Update (SUCCESS)
    deactivate BE
    deactivate ESP32
```

### 2.3 Activity Diagram – Feeding Execution & Monitoring Workflow
```mermaid
stateDiagram-v2
    state "User Interaction Layer" as User {
        direction TB
        [*] --> RequestFeed: Manual Trigger / Schedule Reach
        RequestFeed --> AwaitFeedback: View Status
        ViewLogs: View Feeding History/Analytics
    }

    state "Cloud System Layer" as Cloud {
        direction TB
        RequestFeed --> ValidateRequest: Check Permissions
        
        state Permission_Check <<choice>>
        ValidateRequest --> Permission_Check
        Permission_Check --> ErrorNotify: [Invalid]
        Permission_Check --> CheckDeviceStatus: [Valid]

        state Device_Status_Check <<choice>>
        CheckDeviceStatus --> Device_Status_Check
        Device_Status_Check --> QueueCommand: [Online]
        Device_Status_Check --> BufferCommand: [Offline]

        BufferCommand --> NotifyBuffer: "Feeder Offline: Queued"
        NotifyBuffer --> SyncWait
        SyncWait --> QueueCommand: Device Heartbeat Received
        
        QueueCommand --> DispatchToDevice
        
        ProcessResult --> UpdateDB: INSERT INTO feeding_events
        UpdateDB --> RecomputeAnalytics: Update Daily Totals
        RecomputeAnalytics --> NotifySuccess: Push WebSocket Update
        NotifySuccess --> ViewLogs
    }

    state "IoT Hardware Layer" as IoT {
        direction TB
        DispatchToDevice --> FetchWeights: Tare Load Cell
        FetchWeights --> StartServo: Activate Motor
        
        state Dispensing_Loop {
            [*] --> ReadSensor: HX711 Polling
            ReadSensor --> CompareWeight: current >= target?
            
            state Weight_Reached <<choice>>
            CompareWeight --> Weight_Reached
            Weight_Reached --> ReadSensor: [No]
            Weight_Reached --> StopServo: [Yes]
        }
        
        StopServo --> DetectAnomaly: Compare expected vs. actual
        
        state Anomaly_Check <<choice>>
        DetectAnomaly --> Anomaly_Check
        Anomaly_Check --> ReportError: [Mismatched/Stuck]
        Anomaly_Check --> ProcessResult: [Within Tolerance]
    }
```

## 3. Documentation Draft Sections

### 5.1 Use Case Diagram – Feeding & Monitoring Subsystem
**Purpose:**
This diagram identifies the functional requirements associated with the core operation of the pet feeder: the dispensing of food and the subsequent analysis of consumption data.

**Subsystem Representation:**
It represents the internal logic of the "Feeding, Monitoring & Analytics" subsystem, bridging user intent with hardware execution and data visualization.

**Explanation of Key Elements:**
- **IoT Feeder Actor:** Now explicitly stereotyped to denote its role as an external system component providing feedback.
- **Analytics Extension:** Visualizes how optional data export functionality builds upon basic history viewing.

**System Design Decisions:**
The design ensures that all feeding triggers (manual or scheduled) are captured and logged centrally, allowing for unified analytics across all user touchpoints.

---

### 5.2 Sequence Diagram – Closed-Loop Feeding Operation
**Purpose:**
To detail the precise interaction between the cloud backend and the physical hardware during a dispensing event, emphasizing the importance of the load cell feedback.

**Subsystem Representation:**
Represents the critical "Closed-Loop Control" feature required for the project.

**Explanation of Key Elements:**
- **autonumber & Activation Bars:** Tracks the temporal flow and resource engagement across the cloud-to-hardware bridge.
- **Closed-Loop Loop Block:** Formally models the iterative sensor check that ensures dispensing accuracy.

**System Design Decisions:**
Utilizing a polling mechanism for the ESP32 ensures the system can bypass restricted network environments (NAT/Firewalls) while maintaining the integrity of command delivery.

---

### 5.3 Activity Diagram – Feeding Schedule & Execution Subsystem
**Purpose:**
To map the logical flow of a scheduled event using swimlanes to separate hardware, queue, and scheduling logic.

**Subsystem Representation:**
Represents the "Scheduling & Reliability" logic of the system.

**Explanation of Key Elements:**
- **Swimlanes (System, Queue, IoT):** Clearly delineates the boundary between cloud processing and edge execution.
- **Decision Node:** Handles the critical contingency of device offline status.

**System Design Decisions:**
The asynchronous queuing strategy allows for "fire and forget" scheduling from the user's perspective, with the system guaranteeing eventual execution upon device heartbeat.
