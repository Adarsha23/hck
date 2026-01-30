# Supabase Backend Setup Guide

## Overview
This guide will help you set up the Supabase backend for the Smart Pet Feeder project.

## Prerequisites
- Node.js and npm installed
- A Supabase account (free tier is sufficient)

## Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Fill in the details:
   - **Project Name**: smart-pet-feeder
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose closest to your location
4. Wait for the project to be created (~2 minutes)

## Step 2: Get Your API Credentials

1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy the following values:
   - **Project URL** (under "Project URL")
   - **anon/public key** (under "Project API keys")

## Step 3: Configure Environment Variables

1. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Supabase credentials:
   ```env
   VITE_SUPABASE_URL=https://your-project-id.supabase.co
   VITE_SUPABASE_ANON_KEY=your-anon-key-here
   ```

3. **IMPORTANT**: Add `.env` to `.gitignore` (it should already be there)

## Step 4: Run Database Migrations

1. In your Supabase dashboard, go to **SQL Editor**
2. Click "New Query"
3. Copy the entire contents of `supabase/migrations/001_initial_schema.sql`
4. Paste into the SQL editor
5. Click "Run" to execute the migration
6. You should see "Success. No rows returned" message

## Step 5: Verify Database Setup

1. Go to **Table Editor** in Supabase dashboard
2. You should see the following tables:
   - `devices`
   - `pet_profiles`
   - `feeding_events`
   - `command_queue`
   - `notifications`
   - `device_sensors`
   - `device_shared_access`

## Step 6: Enable Realtime (Optional but Recommended)

1. Go to **Database** → **Replication**
2. Enable replication for the following tables:
   - `devices`
   - `feeding_events`
   - `command_queue`
   - `notifications`
3. This allows real-time subscriptions to work

## Step 7: Test the Connection

1. Start your development server:
   ```bash
   npm run dev
   ```

2. The app should now connect to Supabase
3. Try signing up a new user to test authentication

## Architecture Overview

### Database Tables

- **devices**: Stores feeder devices with serial numbers and pairing codes
- **pet_profiles**: Pet information (name, breed, age, weight, photo)
- **feeding_events**: Log of all feeding attempts with target/actual grams
- **command_queue**: Offline-first command queue for device control
- **notifications**: User notifications for events and alerts
- **device_sensors**: Sensor data (food level, water level, etc.)
- **device_shared_access**: Multi-caregiver access control

### Service Layer

All backend interactions are handled through service modules in `src/services/`:

- **authService.js**: User authentication (signup, login, logout)
- **deviceService.js**: Device management and registration
- **commandService.js**: Command queue operations (feed, pause, resume)
- **feedingService.js**: Feeding events and analytics
- **notificationService.js**: User notifications

### Offline Command Queuing

When you press the feed button:
1. Command is inserted into `command_queue` with status "PENDING"
2. ESP32 polls for pending commands when online
3. Device updates status to "DELIVERED" → "EXECUTED"
4. Real-time subscriptions notify the web app of status changes

### Security

- **Row Level Security (RLS)**: Users can only access their own data
- **Authentication**: JWT tokens with auto-refresh
- **Idempotency**: Commands use unique tokens to prevent duplicates
- **Encryption**: All communication over HTTPS/TLS

## Common Issues

### Issue: "Missing Supabase environment variables"
**Solution**: Make sure `.env` file exists and contains valid credentials

### Issue: Tables not showing in Supabase
**Solution**: Re-run the SQL migration in the SQL Editor

### Issue: Real-time subscriptions not working
**Solution**: Enable replication for tables in Database → Replication

### Issue: Authentication errors
**Solution**: Check that your Supabase URL and anon key are correct

## Next Steps

1. Update existing authentication to use Supabase Auth
2. Integrate command queue with feeder controls
3. Add real-time status updates to dashboard
4. Implement feeding history and analytics
5. Test offline command queuing

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase JavaScript Client](https://supabase.com/docs/reference/javascript/introduction)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
