# Subsystem A: User & Pet Management

## 1. Diagrams Chosen
- Use Case Diagram – User & Pet Management
- Sequence Diagram – User Registration & Email Verification
- Activity Diagram – Pet Profile Creation & Validation

## 2. Mermaid Diagrams

### 2.1 Use Case Diagram – User & Pet Management
```mermaid
graph TD
    %% Actors with STEREOTYPE notation
    A1["Pet Owner\n&lt;&lt;Actor&gt;&gt;"]
    A2["Shared User\n&lt;&lt;Actor&gt;&gt;"]
    A3["Email Service\n&lt;&lt;Actor&gt;&gt;"]
    A4["Supabase Auth\n&lt;&lt;Actor&gt;&gt;"]

    %% Boundaries
    subgraph User_Management ["Subsystem A: User & Pet Management"]
        UC1(("Register Account"))
        UC2(("Login/Auth"))
        UC3(("Verify Email"))
        UC4(("Update Profile"))
        UC5(("Create Pet Profile"))
        UC6(("Update Pet Profile"))
        UC7(("View Pet Details"))
        UC8(("Upload Pet Photo"))
        UC9(("Grant Shared Access"))
    end

    %% Relationships
    A1 --- UC1
    A1 --- UC2
    A1 --- UC4
    A1 --- UC5
    A1 --- UC6
    A1 --- UC7
    A1 --- UC8
    A1 --- UC9

    A2 --- UC2
    A2 --- UC7

    UC1 -.->|&lt;&lt;include&gt;&gt;| UC3
    UC2 -.->|&lt;&lt;include&gt;&gt;| UC3
    UC5 -.->|&lt;&lt;include&gt;&gt;| UC8
    
    UC3 --- A3
    UC2 --- A4

    %% Styling
    classDef actor fill:#f5f5f5,stroke:#333,stroke-width:2px;
    classDef usecase fill:#ffffff,stroke:#333,stroke-width:1px;
    class A1,A2,A3,A4 actor
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9 usecase
```

### 2.2 Sequence Diagram – User Registration & Verification
```mermaid
sequenceDiagram
    autonumber
    actor User as Pet Owner
    participant Web as Web/Mobile Client
    participant Auth as Supabase Auth
    participant DB as PostgreSQL Database
    participant Email as Email Service

    User->>Web: Input Registration Details
    activate Web
    Web->>Auth: signUp(email, password, metadata)
    activate Auth
    Auth->>DB: Create User Record (unverified)
    activate DB
    DB-->>Auth: Record Created
    deactivate DB
    Auth->>Email: Send Verification Link
    activate Email
    Email-->>User: Receive Verification Email
    deactivate Email
    Auth-->>Web: Success Response
    deactivate Auth
    deactivate Web

    User->>Web: Click Verification Link
    activate Web
    Web->>Auth: confirmEmail(token)
    activate Auth
    Auth->>DB: Update email_confirmed_at
    activate DB
    DB-->>Auth: Update Success
    deactivate DB
    Auth-->>Web: Success & JWT Session
    deactivate Auth
    Web-->>User: Redirect to Onboarding/Dashboard
    deactivate Web
```

### 2.3 Activity Diagram – Pet Profile Creation
```mermaid
stateDiagram-v2
    state "User" as S1 {
        direction TB
        [*] --> StartCreation
        StartCreation --> InputDetails: Fills name, breed, age
        InputDetails --> SuccessUI: Sees Profile Created
    }

    state "System" as S2 {
        direction TB
        InputDetails --> ValidateData: Front-end Validation
        state Validation_Check <<choice>>
        ValidateData --> Validation_Check
        Validation_Check --> StartCreation: [Invalid]
        Validation_Check --> PhotoUpload: [Valid]
        
        PhotoUpload --> UploadToStorage: Upload to Storage
        GetURL --> SaveToDB: INSERT INTO pet_profiles
        SaveToDB --> SuccessUI
    }

    state "Supabase Storage" as S3 {
        direction TB
        UploadToStorage --> GetURL: Receive Public URL
    }
```

## 3. Documentation Draft Sections

### 4.1 Use Case Diagram – User & Pet Management Subsystem
**Purpose:** 
The Use Case diagram for the User & Pet Management subsystem defines the interactions between the primary actors (Pet Owner and Shared User) and the system's core administrative functions. It establishes the functional boundaries for identity management and pet data administration.

**Subsystem Representation:**
This diagram represents the "User & Pet Management" subsystem, focusing on onboarding, authentication, and the lifecycle of pet profiles.

**Explanation of Key Elements:**
- **Pet Owner:** The primary actor with full control over registration and pet profiles.
- **Shared User:** An actor with restricted access, primarily focused on viewing pet data and monitoring.
- **Supabase Auth / Email Service:** External systems that facilitate secure authentication and communication.
- **Include Relationships:** Essential dependencies such as requiring email verification before full access is granted to accounts or pet profiles.

**System Design Decisions:**
The inclusion of a "Shared User" actor supports the requirement for family-based pet care. By separating pet profile management into its own subsystem, the design ensures that pet-related data is decoupled from IoT hardware operations, improving maintainability.

---

### 4.2 Sequence Diagram – User Registration & Verification
**Purpose:**
This diagram illustrates the chronological flow of messages between the user, the application frontend, and the backend services during the critical registration phase.

**Subsystem Representation:**
It details the operational flow of the Authentication module within Subsystem A.

**Explanation of Key Elements:**
- **Supabase Auth:** Centralized authentication provider managing the user state.
- **JWT Session:** The token-based security mechanism returned upon successful verification.
- **Activation Bars:** Clearly show the processing time for each system component.

**System Design Decisions:**
The design enforces email verification as a mandatory step before the user can interact with hardware. This prevents orphaned or unverified accounts from consuming system resources and ensures a higher level of security.

---

### 4.3 Activity Diagram – Pet Profile Creation Subsystem
**Purpose:**
To model the step-by-step workflow and logic required to successfully register a new pet within the system using swimlanes to denote responsibility.

**Subsystem Representation:**
Represents the Data Entry and Storage logic for pet profiles.

**Explanation of Key Elements:**
- **Swimlanes (User, System, Supabase Storage):** Explicitly identifies which part of the infrastructure is responsible for each action.
- **Validation Choice:** Represents the front-end logic that ensures data integrity before network calls.

**System Design Decisions:**
The decision to separate photo storage from metadata storage (using storage URLs) optimizes database performance and leverages edge CDNs for faster image loading.
