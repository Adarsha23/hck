

## Context

You have access to my project proposal and literature review. This prompt provides the **technical implementation details** that are NOT in those documents, including the exact technology stack, database schema, backend architecture, and system workflows that have been implemented.

---

## Project Overview

**Project Name**: IoT-Enabled Smart Pet Feeder with Closed-Loop Control  
**Type**: Final Year Project (FYP) - IoT System with Web Application  
**Current Status**: Backend complete, Frontend functional, ESP32 integration pending

---

## COMPLETE TECHNOLOGY STACK

### Frontend Stack
- **Framework**: React 19.2.0
- **Build Tool**: Vite (Rolldown-Vite 7.2.5)
- **Routing**: React Router DOM 7.9.6
- **Styling**: Vanilla CSS (NO Tailwind in main app, only for landing page)
- **State Management**: React Context API
- **Icons**: Lucide React 0.554.0
- **Charts**: Recharts 3.4.1

### Backend Stack (Supabase Platform)
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: Supabase Auth (JWT tokens + Email verification)
- **Real-time**: Supabase Realtime (WebSocket subscriptions)
- **Storage**: Supabase Storage (for pet photos - future)
- **API**: Auto-generated REST API from Supabase
- **Security**: Row-Level Security (RLS) policies at database level

### IoT Hardware Stack (Planned)
- **Microcontroller**: ESP32 (WiFi-enabled)
- **Weight Sensor**: HX711 Load Cell Amplifier
- **Actuator**: Servo Motor (food dispenser mechanism)
- **Level Sensors**: HC-SR04 Ultrasonic Sensors (food/water level detection)
- **Firmware**: Arduino Core for ESP32
- **Communication**: HTTP/HTTPS REST API calls to Supabase

### Development Tools
- **Package Manager**: npm
- **Version Control**: Git + GitHub
- **Environment**: Node.js
- **Linting**: ESLint 9.39.1

---

## COMPLETE DATABASE SCHEMA

### Tables (7 Total)

#### 1. **auth.users** (Managed by Supabase Auth)
```
- id: UUID (PK)
- email: VARCHAR
- encrypted_password: VARCHAR
- email_confirmed_at: TIMESTAMP
- raw_user_meta_data: JSONB (stores user's full name)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

#### 2. **devices** (Feeder Hardware Units)
```
- id: UUID (PK)
- serial_number: VARCHAR(50) UNIQUE NOT NULL
- pairing_code_hash: VARCHAR(255) NOT NULL
- owner_id: UUID (FK → auth.users.id) ON DELETE CASCADE
- device_name: VARCHAR(100)
- status: VARCHAR(20) CHECK IN ('ONLINE', 'OFFLINE', 'ERROR')
- last_seen_at: TIMESTAMP WITH TIME ZONE
- calibration_data: JSONB
- firmware_version: VARCHAR(20)
- created_at: TIMESTAMP WITH TIME ZONE
- updated_at: TIMESTAMP WITH TIME ZONE
```
**Indexes**: owner_id, serial_number, status

#### 3. **pet_profiles** (Pet Information)
```
- id: UUID (PK)
- user_id: UUID (FK → auth.users.id) ON DELETE CASCADE
- name: VARCHAR(100) NOT NULL
- breed: VARCHAR(100)
- age: INTEGER
- weight: DECIMAL(5,2) -- in kg
- height: DECIMAL(5,2) -- in cm
- photo_url: TEXT
- dietary_notes: TEXT
- created_at: TIMESTAMP WITH TIME ZONE
- updated_at: TIMESTAMP WITH TIME ZONE
```
**Indexes**: user_id

#### 4. **feeding_events** (Feeding History Log)
```
- id: UUID (PK)
- device_id: UUID (FK → devices.id) ON DELETE CASCADE
- user_id: UUID (FK → auth.users.id) ON DELETE CASCADE
- pet_id: UUID (FK → pet_profiles.id) ON DELETE SET NULL
- target_grams: DECIMAL(6,2) NOT NULL
- actual_grams: DECIMAL(6,2)
- status: VARCHAR(20) CHECK IN ('PENDING', 'IN_PROGRESS', 'SUCCESS', 'PARTIAL', 'FAILED')
- anomalies: JSONB (array of detected issues)
- duration_seconds: INTEGER
- timestamp: TIMESTAMP WITH TIME ZONE
- completed_at: TIMESTAMP WITH TIME ZONE
```
**Indexes**: device_id, user_id, timestamp DESC, status

#### 5. **command_queue** (Offline Command Queuing)
```
- id: UUID (PK)
- device_id: UUID (FK → devices.id) ON DELETE CASCADE
- user_id: UUID (FK → auth.users.id) ON DELETE CASCADE
- command_type: VARCHAR(20) CHECK IN ('FEED', 'PAUSE', 'RESUME', 'CALIBRATE', 'UPDATE_CONFIG')
- payload: JSONB (contains command parameters like grams, pet_id, etc.)
- status: VARCHAR(20) CHECK IN ('PENDING', 'DELIVERED', 'EXECUTED', 'FAILED', 'CANCELLED')
- idempotency_token: VARCHAR(64) UNIQUE NOT NULL
- priority: INTEGER DEFAULT 0
- created_at: TIMESTAMP WITH TIME ZONE
- delivered_at: TIMESTAMP WITH TIME ZONE
- executed_at: TIMESTAMP WITH TIME ZONE
- error_message: TEXT
```
**Indexes**: (device_id, status) WHERE status='PENDING', idempotency_token, created_at DESC

#### 6. **notifications** (User Alerts)
```
- id: UUID (PK)
- user_id: UUID (FK → auth.users.id) ON DELETE CASCADE
- device_id: UUID (FK → devices.id) ON DELETE CASCADE
- type: VARCHAR(30) CHECK IN ('FEED_COMPLETE', 'FEED_FAILED', 'LOW_FOOD', 'LOW_WATER', 'DEVICE_OFFLINE', 'DEVICE_ONLINE', 'CALIBRATION_NEEDED')
- title: VARCHAR(200) NOT NULL
- message: TEXT NOT NULL
- read: BOOLEAN DEFAULT FALSE
- metadata: JSONB
- created_at: TIMESTAMP WITH TIME ZONE
```
**Indexes**: user_id, (user_id, read), created_at DESC

#### 7. **device_sensors** (Sensor Readings Time-Series)
```
- id: UUID (PK)
- device_id: UUID (FK → devices.id) ON DELETE CASCADE
- sensor_type: VARCHAR(20) CHECK IN ('FOOD_LEVEL', 'WATER_LEVEL', 'TEMPERATURE', 'HUMIDITY')
- value: DECIMAL(10,2) NOT NULL
- unit: VARCHAR(10) NOT NULL
- timestamp: TIMESTAMP WITH TIME ZONE
```
**Indexes**: device_id, timestamp DESC, (device_id, sensor_type, timestamp DESC)

#### 8. **device_shared_access** (Multi-Caregiver Support - Future)
```
- id: UUID (PK)
- device_id: UUID (FK → devices.id) ON DELETE CASCADE
- user_id: UUID (FK → auth.users.id) ON DELETE CASCADE
- role: VARCHAR(20) CHECK IN ('OWNER', 'ADMIN', 'CAREGIVER', 'VIEWER')
- granted_by: UUID (FK → auth.users.id)
- created_at: TIMESTAMP WITH TIME ZONE
- UNIQUE(device_id, user_id)
```
**Indexes**: user_id, device_id

### Database Views (2 Total)

#### 1. **feeding_statistics**
Aggregates feeding data per device:
- total_feedings, total_grams_dispensed, avg_grams_per_feeding
- successful_feedings, failed_feedings, last_feeding_time

#### 2. **daily_feeding_summary**
Daily aggregation:
- feeding_date, feeding_count, total_grams, avg_grams
- first_feeding, last_feeding

### Database Triggers

1. **update_updated_at_column()**: Auto-updates `updated_at` on devices and pet_profiles
2. **notify_feed_completion()**: Auto-creates notifications when feeding status changes to SUCCESS or FAILED
3. **update_device_last_seen()**: Updates device `last_seen_at` and status to ONLINE when command is EXECUTED

---

## FRONTEND ARCHITECTURE

### File Structure
```
src/
├── pages/
│   ├── Home.jsx              # Landing page
│   ├── Login.jsx             # Login with email verification check
│   ├── Signup.jsx            # Signup with Supabase Auth
│   ├── VerifyEmail.jsx       # Email verification waiting screen
│   └── Dashboard.jsx         # Main dashboard (protected route)
├── components/
│   ├── Button.jsx            # Reusable button component
│   ├── Input.jsx             # Reusable input component
│   ├── ProtectedRoute.jsx    # Route guard (checks auth + email verification)
│   ├── FeederCard.jsx        # Device card display
│   ├── AddFeederModal.jsx    # Modal for adding new feeder
│   ├── PetProfileCard.jsx    # Pet profile card
│   ├── PetProfileModal.jsx   # Modal for adding/editing pet
│   └── ImageUpload.jsx       # Image upload component
├── contexts/
│   └── AuthContext.jsx       # Global auth state management
├── services/
│   ├── authService.js        # Authentication logic
│   ├── deviceService.js      # Device CRUD operations
│   ├── commandService.js     # Command queue operations
│   ├── feedingService.js     # Feeding events operations
│   └── notificationService.js # Notification operations
├── lib/
│   └── supabase.js           # Supabase client initialization
├── utils/
│   ├── mockAuth.js           # Mock auth for development
│   ├── feederService.js      # Mock feeder service
│   └── petProfileService.js  # Mock pet profile service
├── App.jsx                   # Main app component with routing
├── main.jsx                  # Entry point
└── index.css                 # Global styles
```

### Service Layer Functions

#### authService.js
- `signUp(email, password, fullName)` - Creates user account
- `signIn(email, password)` - Logs in user
- `signOut()` - Logs out user
- `getCurrentUser()` - Gets current authenticated user
- `onAuthStateChange(callback)` - Listens to auth state changes
- `resendVerificationEmail()` - Resends verification email

#### deviceService.js
- `getUserDevices()` - Fetches all user's devices
- `registerDevice(serialNumber, pairingCode, deviceName)` - Pairs new device
- `updateDeviceName(deviceId, newName)` - Renames device
- `deleteDevice(deviceId)` - Removes device
- `subscribeToDeviceStatus(deviceId, callback)` - Real-time device status updates

#### commandService.js
- `queueFeedCommand(deviceId, grams, petId)` - Queues feed command
- `queuePauseCommand(deviceId)` - Pauses feeding
- `queueResumeCommand(deviceId)` - Resumes feeding
- `queueCalibrateCommand(deviceId)` - Calibrates load cell
- `getPendingCommands(deviceId)` - Gets pending commands
- `subscribeToCommandStatus(commandId, callback)` - Real-time command status

#### feedingService.js
- `getFeedingEvents(deviceId, limit)` - Gets feeding history
- `getFeedingStatistics(deviceId)` - Gets aggregated stats
- `subscribeToDailyFeedings(deviceId, callback)` - Real-time feeding updates

#### notificationService.js
- `getNotifications(limit, unreadOnly)` - Gets notifications
- `markAsRead(notificationId)` - Marks notification as read
- `markAllAsRead()` - Marks all as read
- `deleteNotification(notificationId)` - Deletes notification
- `subscribeToNotifications(callback)` - Real-time notifications

---

## KEY SYSTEM WORKFLOWS

### 1. User Registration & Email Verification Flow
```
1. User fills signup form (email, password, full name)
2. Frontend calls authService.signUp()
3. Supabase creates user with email_confirmed_at = NULL
4. Supabase sends verification email
5. User redirected to /verify-email page
6. User clicks link in email
7. Supabase updates email_confirmed_at = NOW()
8. User redirected to /login?verified=true
9. User logs in
10. ProtectedRoute checks email verification before allowing dashboard access
```

### 2. Offline Command Queuing Flow (CRITICAL FOR FYP)
```
1. User presses "Feed 50g" button in Dashboard
2. Frontend calls commandService.queueFeedCommand(deviceId, 50)
3. Command inserted into command_queue table with status='PENDING'
4. Frontend shows "Command queued" message
5. ESP32 polls database every 10-30 seconds for PENDING commands
6. ESP32 fetches command, updates status='DELIVERED'
7. ESP32 activates servo motor to dispense food
8. Load cell measures actual weight (e.g., 49.8g)
9. ESP32 updates command status='EXECUTED'
10. ESP32 creates feeding_event record with actual_grams=49.8
11. Database trigger creates notification
12. Supabase Realtime pushes update to frontend via WebSocket
13. Frontend displays "Feed complete: 49.8g dispensed"
```

### 3. Closed-Loop Control Flow (Core FYP Feature)
```
1. User requests 50g of food
2. ESP32 receives command
3. ESP32 starts servo motor
4. Load cell continuously reads weight (real-time feedback)
5. When weight >= target (50g), ESP32 stops servo
6. If weight < target after timeout, mark as PARTIAL
7. If weight significantly off, log anomaly in feeding_event.anomalies
8. Report actual_grams back to database
9. Frontend displays comparison: Target vs Actual
```

### 4. Device Pairing Flow
```
1. User clicks "Add Feeder" in Dashboard
2. Modal opens requesting Serial Number + Pairing Code
3. Frontend calls deviceService.registerDevice()
4. Backend verifies pairing code hash matches
5. Device linked to user's account (owner_id = user.id)
6. Device appears in user's dashboard
7. ESP32 can now receive commands from this user
```

### 5. Real-time Status Updates Flow
```
1. Frontend subscribes to device_sensors table for specific device
2. ESP32 periodically inserts sensor readings (food level, water level)
3. Supabase Realtime broadcasts changes via WebSocket
4. Frontend receives update instantly (no polling!)
5. UI updates food/water level indicators
6. If level < threshold, trigger LOW_FOOD or LOW_WATER notification
```

---

## SECURITY ARCHITECTURE

### Row-Level Security (RLS) Policies

**devices table**:
- Users can SELECT their own devices OR devices shared with them
- Users can INSERT only if owner_id = auth.uid()
- Users can UPDATE/DELETE only their own devices

**pet_profiles table**:
- Users can SELECT/INSERT/UPDATE/DELETE only their own profiles (user_id = auth.uid())

**feeding_events table**:
- Users can SELECT events for their devices or shared devices
- Users can INSERT only if user_id = auth.uid()

**command_queue table**:
- Users can SELECT commands for their devices
- Users can INSERT only if user_id = auth.uid()
- Users can UPDATE only their own commands

**notifications table**:
- Users can SELECT/UPDATE/DELETE only their own notifications (user_id = auth.uid())

**device_sensors table**:
- Users can SELECT sensor data only for devices they own

**device_shared_access table**:
- Users can SELECT shared access if they are the user OR device owner
- Only device owners can INSERT/UPDATE/DELETE shared access

### Authentication Flow
1. User logs in → Supabase returns JWT token
2. JWT stored in browser (localStorage via Supabase client)
3. Every API request includes JWT in Authorization header
4. PostgreSQL RLS policies use `auth.uid()` to filter data
5. Users can NEVER access other users' data (enforced at DB level)

---

## ESP32 INTEGRATION PLAN

### ESP32 Responsibilities
1. **Poll for commands** every 10-30 seconds
2. **Execute commands** (feed, calibrate, pause, resume)
3. **Report sensor data** (food level, water level, temperature)
4. **Update device status** (ONLINE when polling, OFFLINE after timeout)
5. **Create feeding events** with actual weight measurements
6. **Handle errors** and report failures

### ESP32 API Endpoints (Supabase REST API)
```
GET /rest/v1/command_queue?device_id=eq.{id}&status=eq.PENDING
PATCH /rest/v1/command_queue?id=eq.{cmd_id}
POST /rest/v1/feeding_events
POST /rest/v1/device_sensors
PATCH /rest/v1/devices?id=eq.{device_id}
```

### ESP32 Authentication
- Each ESP32 has a service role API key (stored in firmware)
- OR device-specific JWT token generated during pairing

---

## DEPLOYMENT ARCHITECTURE

### Current (Development)
- **Frontend**: Vite dev server (localhost:5174)
- **Backend**: Supabase Cloud (hosted PostgreSQL + Auth + Realtime)
- **Database**: Supabase-managed PostgreSQL
- **ESP32**: Not yet deployed

### Future (Production)
- **Frontend**: Vercel or Netlify (static hosting)
- **Backend**: Supabase Cloud (production instance)
- **Custom Domain**: petfeeder.com (example)
- **ESP32**: Deployed in user homes, connecting to Supabase via WiFi

---

## DIAGRAM REQUIREMENTS

Please generate **professional, well-structured, clean, and accurate** Mermaid diagram code for the following 6 diagrams:

### 1. Use Case Diagram
**Show external actors and their interactions:**
- Actors: User (Pet Owner), ESP32 Device, Supabase System, Email Service
- Use cases: Register Account, Verify Email, Login, Add Pet Profile, Pair Device, Queue Feed Command, View Feeding History, Receive Notifications, Calibrate Device, Monitor Food/Water Levels, Share Device Access (future)
- Include relationships: <<include>>, <<extend>>

### 2. Activity Diagram
**Focus on Closed-Loop Control Workflow:**
- Start: User presses "Feed" button
- Decision: Is device online?
  - If NO: Queue command → Wait for device → Retry
  - If YES: Send command immediately
- ESP32 receives command
- Start servo motor
- Loop: Read load cell weight
- Decision: Weight >= target?
  - If NO: Continue dispensing
  - If YES: Stop servo
- Measure final weight
- Decision: Weight within tolerance?
  - If YES: Mark SUCCESS
  - If NO: Mark PARTIAL, log anomaly
- Update database
- Send notification
- End

### 3. Sequence Diagram
**Detailed Feed Command Interaction:**
- Participants: User, Web App (React), AuthContext, commandService, Supabase API, PostgreSQL Database, ESP32, Servo Motor, Load Cell
- Show complete message flow from button press to notification
- Include async operations, database triggers, real-time updates

### 4. Deployment Diagram
**Physical Architecture:**
- Nodes: User's Browser, Vercel Server (Frontend), Supabase Cloud (Backend), PostgreSQL Database, ESP32 Device (User's Home)
- Components: React App, Supabase Client, REST API, Auth Service, Realtime Service, ESP32 Firmware, Sensors (Load Cell, Ultrasonic), Actuators (Servo)
- Connections: HTTPS, WebSocket, WiFi, GPIO

### 5. Class Diagram
**Logical Software Structure:**
- Frontend Classes: AuthContext, DeviceService, CommandService, FeedingService, NotificationService, ProtectedRoute, Dashboard, FeederCard, PetProfileCard
- Backend Classes: User (auth.users), Device, PetProfile, FeedingEvent, Command, Notification, DeviceSensor
- Relationships: associations, compositions, dependencies
- Include key methods and attributes

### 6. Entity Relationship Diagram (ERD)
**Database Structure:**
- All 8 tables: auth.users, devices, pet_profiles, feeding_events, command_queue, notifications, device_sensors, device_shared_access
- Show all columns with data types
- Show primary keys (PK), foreign keys (FK)
- Show relationships with cardinality (1:1, 1:N, N:M)
- Show ON DELETE CASCADE/SET NULL behaviors
- Include indexes where critical

---

## OUTPUT FORMAT

For each diagram, provide:
1. **Diagram Title**
2. **Mermaid Code** (properly formatted, ready to paste into mermaid.live)
3. **Brief Description** of what the diagram shows

Ensure diagrams are:
- ✅ **Professional**: Use proper UML notation
- ✅ **Well-structured**: Logical grouping and layout
- ✅ **Clean**: Not cluttered, readable labels
- ✅ **Accurate**: Reflects actual implementation, not assumptions
- ✅ **Complete**: Includes all critical components and relationships

---

## ADDITIONAL NOTES

- The system uses **offline-first architecture** - commands work even when ESP32 is offline
- **Real-time updates** via WebSocket eliminate need for polling on frontend
- **Row-Level Security** is enforced at database level, not application level
- **Idempotency tokens** prevent duplicate command execution
- **Closed-loop control** uses load cell feedback to ensure accurate dispensing
- **Multi-caregiver support** allows families to share device access (future feature)

---

**Please generate codes for all 6 diagrams now which will be pasted on mermaid. Thank you!**