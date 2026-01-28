# Smart Pet Feeder - System Requirements Specification

## 1. Functional Requirements

### 1.1 User Authentication & Management
- **FR1.1**: System shall allow users to register with email and password
- **FR1.2**: System shall send email verification upon registration
- **FR1.3**: System shall require email verification before granting full access
- **FR1.4**: System shall allow users to login with verified credentials
- **FR1.5**: System shall allow users to reset password via email
- **FR1.6**: System shall allow users to manage their profile information
- **FR1.7**: System shall allow users to logout securely

### 1.2 Pet Profile Management
- **FR2.1**: System shall allow users to create a pet profile
- **FR2.2**: System shall store pet information (name, breed, age, weight, height)
- **FR2.3**: System shall allow users to upload pet photos
- **FR2.4**: System shall allow users to update pet profile information
- **FR2.5**: System shall allow users to delete pet profiles
- **FR2.6**: System shall allow users to view pet details

### 1.3 Device Management
- **FR3.1**: System shall allow users to pair new IoT devices using serial number and pairing code
- **FR3.2**: System shall verify device credentials before pairing
- **FR3.3**: System shall allow users to rename paired devices
- **FR3.4**: System shall display real-time device status (ONLINE/OFFLINE/ERROR)
- **FR3.5**: System shall allow users to unpair devices
- **FR3.6**: System shall allow users to share device access with other users
- **FR3.7**: System shall allow device owners to revoke shared access
- **FR3.8**: System shall allow users to calibrate device load cells
- **FR3.9**: System shall track device last seen timestamp
- **FR3.10**: System shall store device firmware version information

### 1.4 Feeding Operations
- **FR4.1**: System shall allow users to trigger manual feeding
- **FR4.2**: System shall allow users to set feed amount in grams (0-500g)
- **FR4.3**: System shall allow users to schedule recurring feedings
- **FR4.4**: System shall allow users to edit feeding schedules
- **FR4.5**: System shall allow users to cancel scheduled feedings
- **FR4.6**: System shall queue commands when device is offline
- **FR4.7**: System shall execute queued commands when device comes online
- **FR4.8**: System shall allow users to monitor real-time feeding progress
- **FR4.9**: System shall record target vs actual grams dispensed
- **FR4.10**: System shall detect and log feeding anomalies

### 1.5 Closed-Loop Control (Core FYP Feature)
- **FR5.1**: IoT device shall continuously read load cell weight during dispensing
- **FR5.2**: IoT device shall stop servo motor when target weight is reached
- **FR5.3**: IoT device shall handle timeout scenarios (mark as PARTIAL)
- **FR5.4**: IoT device shall validate final weight within ±5% tolerance
- **FR5.5**: IoT device shall mark feeding as FAILED if deviation >10%
- **FR5.6**: IoT device shall log anomalies for out-of-tolerance dispensing
- **FR5.7**: IoT device shall report actual grams dispensed to database

### 1.6 Monitoring & Analytics
- **FR6.1**: System shall display current food level
- **FR6.2**: System shall display current water level
- **FR6.3**: System shall provide daily feeding summary
- **FR6.4**: System shall provide weekly feeding summary
- **FR6.5**: System shall calculate feeding statistics (total, average, success rate)
- **FR6.6**: System shall allow users to export feeding data
- **FR6.7**: System shall display anomaly reports
- **FR6.8**: System shall allow users to set low-level alerts for food/water
- **FR6.9**: System shall track feeding history with timestamps

### 1.7 Notification System
- **FR7.1**: System shall send notifications for feed completion
- **FR7.2**: System shall send notifications for feed failures
- **FR7.3**: System shall send notifications for low food level
- **FR7.4**: System shall send notifications for low water level
- **FR7.5**: System shall send notifications when device goes offline
- **FR7.6**: System shall send notifications when device comes online
- **FR7.7**: System shall send notifications when calibration is needed
- **FR7.8**: System shall allow users to configure notification preferences
- **FR7.9**: System shall allow users to mark notifications as read
- **FR7.10**: System shall allow users to delete notifications

### 1.8 IoT Device Operations
- **FR8.1**: IoT device shall poll for pending commands every 10-30 seconds
- **FR8.2**: IoT device shall execute feed commands from queue
- **FR8.3**: IoT device shall report device status to server
- **FR8.4**: IoT device shall report sensor readings (food level, water level, temperature, humidity)
- **FR8.5**: IoT device shall perform load cell calibration on command
- **FR8.6**: IoT device shall handle error conditions gracefully
- **FR8.7**: IoT device shall update last seen timestamp on each poll
- **FR8.8**: IoT device shall update command status (PENDING → DELIVERED → EXECUTED)

---

## 2. Non-Functional Requirements

### 2.1 Performance Requirements
- **NFR1.1**: System shall respond to user actions within 2 seconds
- **NFR1.2**: Real-time updates shall be delivered within 3 seconds via WebSocket
- **NFR1.3**: IoT device shall poll for commands every 10-30 seconds
- **NFR1.4**: Database queries shall execute within 500ms for 95% of requests
- **NFR1.5**: System shall support up to 1000 concurrent users

### 2.2 Reliability Requirements
- **NFR2.1**: System shall have 99% uptime
- **NFR2.2**: Offline command queuing shall ensure zero command loss
- **NFR2.3**: System shall implement idempotency tokens to prevent duplicate commands
- **NFR2.4**: Database shall implement automatic backups daily
- **NFR2.5**: System shall gracefully handle IoT device disconnections

### 2.3 Security Requirements
- **NFR3.1**: All passwords shall be encrypted using industry-standard hashing
- **NFR3.2**: All API communications shall use HTTPS/TLS encryption
- **NFR3.3**: System shall implement Row-Level Security (RLS) at database level
- **NFR3.4**: JWT tokens shall expire after 24 hours
- **NFR3.5**: Device pairing codes shall be hashed before storage
- **NFR3.6**: Users shall only access their own data (enforced by RLS)
- **NFR3.7**: Email verification shall be mandatory before full system access

### 2.4 Usability Requirements
- **NFR4.1**: User interface shall be intuitive and require no training
- **NFR4.2**: System shall provide clear error messages
- **NFR4.3**: System shall provide visual feedback for all user actions
- **NFR4.4**: Dashboard shall display all critical information at a glance
- **NFR4.5**: Mobile-responsive design for access on all devices

### 2.5 Scalability Requirements
- **NFR5.1**: Database schema shall support multiple devices per user
- **NFR5.2**: Database schema shall support multiple pets per user
- **NFR5.3**: System shall support shared device access for families
- **NFR5.4**: Architecture shall support horizontal scaling

### 2.6 Maintainability Requirements
- **NFR6.1**: Code shall follow consistent naming conventions
- **NFR6.2**: System shall use service layer pattern for separation of concerns
- **NFR6.3**: Database triggers shall automate repetitive tasks
- **NFR6.4**: System shall log all errors for debugging
- **NFR6.5**: Code shall be modular and reusable

### 2.7 Compatibility Requirements
- **NFR7.1**: Web application shall support Chrome, Firefox, Safari, Edge
- **NFR7.2**: IoT device shall support WiFi 802.11 b/g/n (2.4GHz)
- **NFR7.3**: System shall work with ESP32 microcontrollers
- **NFR7.4**: System shall support HX711 load cell amplifiers
- **NFR7.5**: System shall support standard servo motors (SG90/MG996R)

---

## 3. System Constraints

### 3.1 Technical Constraints
- **C1.1**: Frontend must be built with React 19.2.0
- **C1.2**: Backend must use Supabase (PostgreSQL + Auth + Realtime)
- **C1.3**: IoT device must use ESP32 microcontroller
- **C1.4**: Communication protocol must be HTTPS REST API
- **C1.5**: Real-time updates must use WebSocket (Supabase Realtime)

### 3.2 Hardware Constraints
- **C2.1**: Load cell range: 0-5kg
- **C2.2**: Feed amount range: 0-500g per feeding
- **C2.3**: Power supply: 5V/2A DC
- **C2.4**: Servo motor: 180° rotation capability

### 3.3 Data Constraints
- **C3.1**: All timestamps must use UTC with timezone
- **C3.2**: UUIDs must be used for all primary keys
- **C3.3**: Feeding history must be retained indefinitely
- **C3.4**: Sensor data must be timestamped

---

## 4. Interface Requirements

### 4.1 User Interface Requirements
- **IR1.1**: Landing page with project overview
- **IR1.2**: Login/Signup pages with form validation
- **IR1.3**: Email verification waiting screen
- **IR1.4**: Dashboard with device cards and pet profiles
- **IR1.5**: Feeding history with charts and statistics
- **IR1.6**: Notification center with unread indicators
- **IR1.7**: Device management modals
- **IR1.8**: Pet profile management modals

### 4.2 Hardware Interface Requirements
- **IR2.1**: ESP32 GPIO pins for servo motor (PWM)
- **IR2.2**: ESP32 I2C interface for HX711 load cell
- **IR2.3**: ESP32 GPIO pins for ultrasonic sensors (Trigger/Echo)
- **IR2.4**: ESP32 WiFi interface for network communication

### 4.3 Software Interface Requirements
- **IR3.1**: Supabase REST API for CRUD operations
- **IR3.2**: Supabase Auth API for authentication
- **IR3.3**: Supabase Realtime API for WebSocket subscriptions
- **IR3.4**: Email service API for verification emails

### 4.4 Communication Interface Requirements
- **IR4.1**: HTTPS for web app to backend communication
- **IR4.2**: WSS (WebSocket Secure) for real-time updates
- **IR4.3**: WiFi 802.11 for ESP32 connectivity
- **IR4.4**: I2C protocol for load cell communication
- **IR4.5**: PWM signals for servo motor control

---

## 5. Database Requirements

### 5.1 Tables Required
- **DR1.1**: users table (managed by Supabase Auth)
- **DR1.2**: devices table with RLS policies
- **DR1.3**: pet_profiles table with RLS policies
- **DR1.4**: feeding_events table with RLS policies
- **DR1.5**: command_queue table with RLS policies
- **DR1.6**: notifications table with RLS policies
- **DR1.7**: device_sensors table with RLS policies
- **DR1.8**: device_shared_access table with RLS policies

### 5.2 Database Features Required
- **DR2.1**: Automatic timestamp updates via triggers
- **DR2.2**: Automatic notification creation via triggers
- **DR2.3**: Automatic device status updates via triggers
- **DR2.4**: Materialized views for feeding statistics
- **DR2.5**: Indexes on frequently queried columns
- **DR2.6**: Foreign key constraints with CASCADE/SET NULL

---

## 6. Testing Requirements

### 6.1 Unit Testing
- **TR1.1**: Test all service layer functions
- **TR1.2**: Test database triggers
- **TR1.3**: Test RLS policies

### 6.2 Integration Testing
- **TR2.1**: Test complete feed command flow
- **TR2.2**: Test offline command queuing
- **TR2.3**: Test real-time updates
- **TR2.4**: Test email verification flow

### 6.3 System Testing
- **TR3.1**: Test closed-loop control accuracy
- **TR3.2**: Test device pairing process
- **TR3.3**: Test multi-user scenarios
- **TR3.4**: Test error handling

### 6.4 User Acceptance Testing
- **TR4.1**: Verify all use cases work as expected
- **TR4.2**: Verify UI is intuitive
- **TR4.3**: Verify notifications are timely

---

## 7. Documentation Requirements

- **DOC1**: User manual for pet owners
- **DOC2**: Installation guide for IoT device
- **DOC3**: API documentation for developers
- **DOC4**: Database schema documentation
- **DOC5**: System architecture diagrams (UML)
- **DOC6**: Deployment guide

---

**Total Functional Requirements**: 45  
**Total Non-Functional Requirements**: 27  
**Total Constraints**: 11  
**Total Interface Requirements**: 16  
**Total Database Requirements**: 11  
**Total Testing Requirements**: 12  
**Total Documentation Requirements**: 6  

**Grand Total**: 128 Requirements
