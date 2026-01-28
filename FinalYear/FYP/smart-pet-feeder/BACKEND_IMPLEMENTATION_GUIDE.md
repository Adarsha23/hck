# Backend Implementation Guide - Smart Pet Feeder

## What Language/Framework Did I Use for Backend?

I didn't write a traditional backend server in Node.js or Python. Instead, I used **Supabase**, which is a Backend-as-a-Service (BaaS) platform. Here's what that means:

### What is Supabase?

**Supabase** is like Firebase but uses PostgreSQL (a real SQL database) instead of NoSQL. It provides:
- **PostgreSQL Database** - Where all data is stored
- **Authentication System** - Handles user login/signup
- **Auto-generated REST API** - No need to write API endpoints
- **Real-time Subscriptions** - WebSocket connections for live updates
- **Row-Level Security** - Database-level access control

Think of it as getting a complete backend without writing Express.js routes or authentication middleware.

### Why Supabase Instead of Building My Own Backend?

**Time Savings**: Building authentication alone would take 2-3 weeks:
- Password hashing (bcrypt)
- JWT token generation
- Email verification system
- Password reset flow
- Session management

Supabase does all this automatically.

**Security**: Their authentication is battle-tested and secure. If I built my own, I might make security mistakes.

**Real Database**: PostgreSQL is a production-grade database used by Instagram, Spotify, etc. It supports complex queries needed for analytics.

## What is PostgreSQL?

**PostgreSQL** (often called Postgres) is a **relational database management system (RDBMS)**. 

### Simple Explanation:
Think of it like Excel spreadsheets, but much more powerful:
- Each **table** is like a spreadsheet
- Each **row** is a record (like one student)
- Each **column** is a field (like name, age, email)
- **Relationships** connect tables (like students → courses)

### Why PostgreSQL vs MySQL or MongoDB?

**PostgreSQL vs MySQL**:
- Both are SQL databases
- PostgreSQL has better support for JSON data (I use this for storing anomalies, metadata)
- PostgreSQL has more advanced features (triggers, views, RLS)

**PostgreSQL vs MongoDB**:
- MongoDB is NoSQL (no fixed structure)
- PostgreSQL is SQL (structured tables with relationships)
- For my project, I need relationships (users → devices → feeding events)
- SQL is better for analytics queries (daily summaries, statistics)

### What is SQL?

**SQL** = Structured Query Language. It's how you talk to the database.

Example queries I use:
```sql
-- Get all devices owned by current user
SELECT * FROM devices WHERE owner_id = 'user-123';

-- Get feeding history for last 7 days
SELECT * FROM feeding_events 
WHERE device_id = 'device-456' 
AND timestamp > NOW() - INTERVAL '7 days'
ORDER BY timestamp DESC;

-- Calculate average grams dispensed
SELECT AVG(actual_grams) FROM feeding_events 
WHERE status = 'SUCCESS';
```

## What is Authentication (Auth)?

**Authentication** = Proving who you are (like showing your ID card)

### How It Works in My Project:

**1. User Signs Up**:
```
User enters: email + password + name
         ↓
Supabase hashes password (bcrypt algorithm)
         ↓
Stores in database: {email, hashed_password}
         ↓
Sends verification email
```

**2. User Logs In**:
```
User enters: email + password
         ↓
Supabase checks: Does user exist? Is password correct?
         ↓
If yes: Returns JWT token (like a temporary pass)
         ↓
Frontend stores token in localStorage
         ↓
Every API request includes this token
```

**3. JWT Token**:
- **JWT** = JSON Web Token
- It's a long string that proves you're logged in
- Example: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- Contains: user ID, email, expiration time
- Expires after 1 hour (for security)

**4. Email Verification**:
- After signup, user can't login until they verify email
- Prevents fake accounts
- Supabase sends email with unique link
- When clicked, sets `email_confirmed_at` timestamp in database

## How Does the Frontend Talk to Backend?

### REST API (Automatic)

Supabase auto-generates REST API endpoints for every table:

**Example - Get all devices**:
```javascript
// Frontend code
const { data } = await supabase
  .from('devices')
  .select('*')
  .eq('owner_id', userId);

// Behind the scenes, this makes HTTP request:
// GET https://yourproject.supabase.co/rest/v1/devices?owner_id=eq.user-123
// Headers: { apikey: 'xxx', Authorization: 'Bearer jwt-token' }
```

**Example - Create feeding command**:
```javascript
const { data } = await supabase
  .from('command_queue')
  .insert({
    device_id: 'device-123',
    command_type: 'FEED',
    payload: { grams: 50 },
    status: 'PENDING'
  });

// Behind the scenes:
// POST https://yourproject.supabase.co/rest/v1/command_queue
// Body: { device_id: '...', command_type: 'FEED', ... }
```

### Real-time Subscriptions (WebSocket)

For live updates, I use WebSocket connections:

```javascript
// Subscribe to command status changes
const subscription = supabase
  .channel('command-updates')
  .on('postgres_changes', 
    { 
      event: 'UPDATE', 
      schema: 'public', 
      table: 'command_queue',
      filter: `id=eq.${commandId}`
    }, 
    (payload) => {
      console.log('Command updated!', payload.new.status);
      // Show notification to user
    }
  )
  .subscribe();
```

**How it works**:
1. Frontend opens WebSocket connection to Supabase
2. Subscribes to changes on `command_queue` table
3. When ESP32 updates command status, database triggers WebSocket event
4. Frontend receives update instantly (no polling needed)

## Database Schema Explained

### Tables I Created:

**1. users** (Managed by Supabase Auth)
- Stores: email, password (hashed), name
- Created automatically when user signs up

**2. devices**
- Each row = one pet feeder hardware unit
- Columns: serial_number, owner_id, device_name, status, last_seen_at
- Relationship: Each device belongs to one user

**3. pet_profiles**
- Stores pet information
- Columns: name, breed, age, weight, photo_url
- Relationship: Each pet belongs to one user

**4. feeding_events**
- Log of every feeding attempt
- Columns: target_grams, actual_grams, status, timestamp
- This is my audit trail - shows accuracy of closed-loop control

**5. command_queue** ⭐ **Most Important**
- Enables offline functionality
- Columns: command_type, payload, status, idempotency_token
- Status flow: PENDING → DELIVERED → EXECUTED

**6. notifications**
- User alerts
- Auto-created by database triggers

**7. device_sensors**
- Time-series data from ultrasonic sensors
- Tracks food level, water level over time

### What is Row-Level Security (RLS)?

**Problem**: Without RLS, any logged-in user could query ALL devices:
```sql
SELECT * FROM devices;  -- Returns EVERYONE's devices ❌
```

**Solution**: RLS policies filter data automatically:
```sql
CREATE POLICY "Users see only their devices"
ON devices FOR SELECT
USING (auth.uid() = owner_id);
```

Now when user queries:
```sql
SELECT * FROM devices;  -- Returns ONLY their devices ✅
```

PostgreSQL automatically adds `WHERE owner_id = current_user_id`.

**Why this is powerful**:
- Security enforced at database level
- Can't be bypassed from frontend
- Even if someone steals API key, they can only see their own data

## Offline Command Queuing - Core Feature

### The Problem:
ESP32 might be offline when user presses "Feed" button (WiFi down, unplugged, etc.)

### Bad Solution:
Show error "Device offline, try again later"
- User has to remember
- Command is lost

### My Solution:
Queue commands in database:

**Step 1**: User presses Feed
```javascript
await supabase.from('command_queue').insert({
  device_id: 'device-123',
  command_type: 'FEED',
  payload: { grams: 50 },
  status: 'PENDING'  // Saved even if device offline
});
```

**Step 2**: ESP32 polls every 10-30 seconds
```cpp
// ESP32 code (Arduino)
String url = "https://supabase.co/rest/v1/command_queue";
url += "?device_id=eq." + deviceId;
url += "&status=eq.PENDING";

HTTPClient http;
http.GET(url);  // Fetches pending commands
```

**Step 3**: ESP32 executes when online
```cpp
// Update status
PATCH /command_queue { status: 'DELIVERED' }

// Dispense food
runServo(50);

// Report completion
PATCH /command_queue { status: 'EXECUTED' }
POST /feeding_events { actual_grams: 49.8 }
```

**Step 4**: User gets real-time notification
```javascript
// Frontend receives WebSocket update
"Feed complete: 49.8g dispensed"
```

## Database Triggers - Automation

### What is a Trigger?

A **trigger** is code that runs automatically when data changes.

**Example 1**: Auto-update timestamps
```sql
CREATE TRIGGER update_devices_updated_at
BEFORE UPDATE ON devices
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

Every time a device is updated, `updated_at` column is set to NOW().

**Example 2**: Auto-create notifications
```sql
CREATE TRIGGER notify_feed_completion
AFTER INSERT ON feeding_events
FOR EACH ROW
WHEN (NEW.status = 'SUCCESS')
EXECUTE FUNCTION create_notification();
```

When feeding succeeds, automatically insert notification for user.

## Service Layer Pattern

I organized code into **services** - reusable functions for each feature:

**authService.js** - Authentication
```javascript
export const signUp = async (email, password, name)
export const signIn = async (email, password)
export const signOut = async ()
```

**deviceService.js** - Device management
```javascript
export const getUserDevices = async ()
export const registerDevice = async (serialNumber, pairingCode)
export const updateDeviceName = async (id, name)
```

**commandService.js** - Command queue
```javascript
export const queueFeedCommand = async (deviceId, grams)
export const getPendingCommands = async (deviceId)
```

**Why separate files?**
- Reusable across components
- Easier to test
- Single source of truth for API calls

## Summary - What I Built

**Backend Infrastructure**:
- PostgreSQL database with 7 tables
- Row-Level Security for data protection
- Auto-generated REST API
- Real-time WebSocket subscriptions

**Key Features**:
- User authentication with email verification
- Offline command queuing (core FYP requirement)
- Database triggers for automation
- Service layer for clean code organization

**Technologies**:
- Supabase (Backend-as-a-Service)
- PostgreSQL (SQL database)
- JWT (Authentication tokens)
- WebSocket (Real-time updates)

**Why These Choices**:
- Saves 3-4 weeks of development time
- Production-grade security
- Supports offline functionality
- Enables real-time updates
- Free for student projects
