# Smart Pet Feeder - Backend Integration

##  Backend Stack Implemented

My Smart Pet Feeder now has a complete **Supabase** backend with:

- **PostgreSQL Database** with 7 tables and analytics views
-  **Authentication** with JWT tokens and session management
-  **Offline Command Queuing** for reliable device control
-  **Real-time Subscriptions** for live updates
- **Row-Level Security** for data protection
-  **Service Layer** with 5 specialized modules

## 📁 Project Structure

```
smart-pet-feeder/
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql    # Complete database schema
├── src/
│   ├── lib/
│   │   └── supabase.js               # Supabase client config
│   ├── services/
│   │   ├── authService.js            # Authentication
│   │   ├── deviceService.js          # Device management
│   │   ├── commandService.js         # Command queue
│   │   ├── feedingService.js         # Feeding events
│   │   └── notificationService.js    # Notifications
│   └── contexts/
│       └── AuthContext.jsx           # Auth context (to be updated)
├── .env.example                      # Environment template
├── SUPABASE_SETUP.md                 # Setup instructions
└── README.md                         # This file
```

## 🚀 Quick Start

### 1. Set Up Supabase

Follow the detailed instructions in [`SUPABASE_SETUP.md`](./SUPABASE_SETUP.md)

**Quick version:**
1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Copy `.env.example` to `.env` and add your credentials
3. Run the SQL migration in Supabase SQL Editor
4. Enable realtime for tables

### 2. Install Dependencies

```bash
npm install
```

Dependencies added:
- `@supabase/supabase-js` - Supabase client
- `uuid` - For generating idempotency tokens

### 3. Run Development Server

```bash
npm run dev
```

## 🔑 Key Features

### Offline Command Queuing

The most important feature for your FYP requirements:

**Problem**: What happens when you press "Feed" but the ESP32 is offline?

**Solution**: Commands are stored in a database queue with these states:
- `PENDING` → Command created, waiting for device
- `DELIVERED` → Device received the command
- `EXECUTED` → Device completed the action
- `FAILED` → Something went wrong

**Flow**:
```
User presses Feed → Command saved to database (PENDING)
                  ↓
ESP32 comes online → Fetches pending commands
                  ↓
ESP32 executes → Updates status to EXECUTED
                  ↓
Web app receives real-time update → Shows success
```

### Real-time Updates

Using Supabase Realtime, your web app gets instant updates when:
- Device status changes (ONLINE/OFFLINE)
- Feeding completes
- New notifications arrive
- Command status updates

### Security

- **Row-Level Security (RLS)**: Users can only see their own data
- **JWT Authentication**: Secure token-based auth
- **Idempotency Tokens**: Prevent duplicate commands
- **HTTPS**: All communication encrypted

## 📊 Database Schema

### Core Tables

1. **devices** - Feeder hardware units
   - Serial number + pairing code authentication
   - Online/offline status tracking
   - Calibration data storage

2. **pet_profiles** - Pet information
   - Name, breed, age, weight, height
   - Photo storage
   - Dietary notes

3. **feeding_events** - Feeding history
   - Target vs actual grams dispensed
   - Success/failure status
   - Anomaly tracking
   - Duration metrics

4. **command_queue** - Offline-first commands
   - Feed, pause, resume, calibrate
   - Idempotency tokens
   - Priority ordering
   - Status tracking

5. **notifications** - User alerts
   - Feed complete/failed
   - Low food/water
   - Device online/offline

6. **device_sensors** - Sensor readings
   - Food level, water level
   - Temperature, humidity
   - Time-series data

7. **device_shared_access** - Multi-caregiver support
   - Role-based access (Owner, Admin, Caregiver, Viewer)
   - Shared device management

## 🛠️ Service Layer API

### Authentication (`authService.js`)

```javascript
import { signUp, signIn, signOut, getCurrentUser } from './services/authService';

// Sign up
const { data, error } = await signUp('email@example.com', 'password', 'Full Name');

// Sign in
const { data, error } = await signIn('email@example.com', 'password');

// Get current user
const { user, error } = await getCurrentUser();

// Sign out
await signOut();
```

### Device Management (`deviceService.js`)

```javascript
import { getUserDevices, registerDevice, subscribeToDeviceStatus } from './services/deviceService';

// Get all devices
const { data: devices } = await getUserDevices();

// Register new device
const { data: device } = await registerDevice('SN12345', 'PAIR123', 'Kitchen Feeder');

// Subscribe to status changes
const subscription = subscribeToDeviceStatus(deviceId, (device) => {
  console.log('Device status:', device.status);
});
```

### Command Queue (`commandService.js`)

```javascript
import { queueFeedCommand, subscribeToCommandStatus } from './services/commandService';

// Queue a feed command (works offline!)
const { data: command } = await queueFeedCommand(deviceId, 50); // 50 grams

// Subscribe to command status
const subscription = subscribeToCommandStatus(command.id, (cmd) => {
  console.log('Command status:', cmd.status); // PENDING → DELIVERED → EXECUTED
});
```

### Feeding Events (`feedingService.js`)

```javascript
import { getFeedingEvents, getFeedingStatistics } from './services/feedingService';

// Get feeding history
const { data: events } = await getFeedingEvents(deviceId, 50);

// Get statistics
const { data: stats } = await getFeedingStatistics(deviceId);
// Returns: total_feedings, avg_grams_per_feeding, success rate, etc.
```

### Notifications (`notificationService.js`)

```javascript
import { getNotifications, markAsRead, subscribeToNotifications } from './services/notificationService';

// Get notifications
const { data: notifications } = await getNotifications(50, true); // unread only

// Mark as read
await markAsRead(notificationId);

// Subscribe to new notifications
const subscription = subscribeToNotifications((notification) => {
  console.log('New notification:', notification.title);
});
```

## 🔄 Next Steps

### 1. Update Authentication Context

Replace the mock authentication in `src/contexts/AuthContext.jsx` with Supabase Auth:

```javascript
import { signIn, signUp, signOut, getCurrentUser, onAuthStateChange } from '../services/authService';
```

### 2. Integrate Command Queue

Update your feeder controls to use the command queue:

```javascript
// In your FeederCard or Dashboard component
import { queueFeedCommand } from '../services/commandService';

const handleFeed = async () => {
  const { data, error } = await queueFeedCommand(deviceId, 50);
  if (!error) {
    toast.success('Feed command queued!');
  }
};
```

### 3. Add Real-time Status

Show live device status in your dashboard:

```javascript
import { subscribeToDeviceStatus } from '../services/deviceService';

useEffect(() => {
  const subscription = subscribeToDeviceStatus(deviceId, (device) => {
    setDeviceStatus(device.status);
  });

  return () => subscription.unsubscribe();
}, [deviceId]);
```

### 4. Display Feeding History

Create a feeding history component:

```javascript
import { getFeedingEvents } from '../services/feedingService';

const [events, setEvents] = useState([]);

useEffect(() => {
  const fetchEvents = async () => {
    const { data } = await getFeedingEvents(deviceId);
    setEvents(data);
  };
  fetchEvents();
}, [deviceId]);
```

## 📝 ESP32 Integration

The ESP32 will need to:

1. **Poll for commands** (every 10-30 seconds):
   ```
   GET /rest/v1/command_queue?device_id=eq.{id}&status=eq.PENDING
   ```

2. **Update command status**:
   ```
   PATCH /rest/v1/command_queue?id=eq.{cmd_id}
   Body: { "status": "DELIVERED" }
   ```

3. **Create feeding events**:
   ```
   POST /rest/v1/feeding_events
   Body: { "device_id": "...", "actual_grams": 49.8, "status": "SUCCESS" }
   ```

4. **Update device status**:
   ```
   PATCH /rest/v1/devices?id=eq.{device_id}
   Body: { "status": "ONLINE", "last_seen_at": "2025-12-03T19:00:00Z" }
   ```



## 📚 Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase JavaScript Client](https://supabase.com/docs/reference/javascript/introduction)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [Realtime Subscriptions](https://supabase.com/docs/guides/realtime)

## 🐛 Troubleshooting

See [`SUPABASE_SETUP.md`](./SUPABASE_SETUP.md) for common issues and solutions.

## 📄 License

MIT License - see LICENSE file for details
