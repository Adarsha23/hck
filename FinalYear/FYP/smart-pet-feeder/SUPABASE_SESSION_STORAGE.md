# Supabase Session Storage Explanation

## What's Being Stored

When you set `persistSession: true` in the Supabase client configuration, Supabase **automatically** stores the following in **localStorage**:

### Key: `sb-<project-ref>-auth-token`

**Contains:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "expires_at": 1701619200,
  "refresh_token": "v1.MRjVsZXNzIHRva2Vu...",
  "user": {
    "id": "32fce5ca-13d0-4215-b297-39a86b6b46ad",
    "email": "user@example.com",
    "email_confirmed_at": "2025-12-03T19:00:00Z",  // ← THIS IS THE ISSUE
    "created_at": "2025-12-03T18:55:00Z",
    "user_metadata": {
      "full_name": "Test User"
    }
  }
}
```

## The Problem You Experienced

### Scenario:
1. **Day 1**: You sign up with `test@example.com`
2. Supabase creates user in database
3. You verify email → `email_confirmed_at` is set
4. **Session stored in localStorage** with `email_confirmed_at: "2025-12-03T19:00:00Z"`

5. **Day 2**: You delete user from Supabase dashboard
6. Database no longer has this user
7. **BUT** localStorage still has the old session!

8. You try to sign up again with `test@example.com`
9. Supabase checks localStorage first
10. Finds old session with `email_confirmed_at` already set
11. **Thinks email is verified** even though user doesn't exist in DB!

### Why Incognito Works:
- Incognito mode = **fresh localStorage**
- No cached session
- Supabase treats it as a completely new user
- Email verification required

## The Fix Options

### Option 1: Keep persistSession (Recommended)
**Pros:**
- Users stay logged in after closing browser
- Better UX
- Standard behavior

**Cons:**
- Need to handle session cleanup properly

**What to do:**
- Always call `supabase.auth.signOut()` before testing with same email
- Or clear localStorage manually: `localStorage.clear()`

### Option 2: Disable persistSession (Not Recommended)
```javascript
// supabase.js
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
        autoRefreshToken: true,
        persistSession: false,  // ← Users logged out on page refresh
        detectSessionInUrl: true,
    },
});
```

**Pros:**
- No localStorage issues during development

**Cons:**
- Users logged out every time they refresh page
- Terrible UX
- Not production-ready

### Option 3: Use sessionStorage Instead
```javascript
// supabase.js
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
        autoRefreshToken: true,
        persistSession: true,
        storage: window.sessionStorage,  // ← Cleared when tab closes
        detectSessionInUrl: true,
    },
});
```

**Pros:**
- Session cleared when browser tab closes
- Easier testing

**Cons:**
- Users logged out when they close tab (not just browser)
- Still not great UX

## What You Should Do

### For Development/Testing:
**Before testing signup with same email:**
```javascript
// In browser console:
localStorage.clear();
// OR
localStorage.removeItem('sb-tjzcpepvnebwcoqobrlt-auth-token');
```

**Or use Incognito mode** (which you already discovered!)

### For Production:
**Keep `persistSession: true`** - this is the correct behavior!

Users SHOULD stay logged in after closing browser. The issue you experienced only happens because you're:
1. Deleting users from database manually
2. Trying to sign up with same email immediately
3. Not clearing localStorage between tests

**In real production:**
- Users won't delete themselves from database
- If they sign up → verify → use app normally
- Session persistence is GOOD

## How to Check What's Stored

### In Browser DevTools:
1. Press F12
2. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
3. Expand **Local Storage**
4. Click on `http://localhost:5174`
5. Look for key starting with `sb-`

You'll see the entire session object with:
- JWT tokens
- User data
- **email_confirmed_at** timestamp

## Summary

✅ **Yes, Supabase uses localStorage** (when `persistSession: true`)
✅ **This is CORRECT behavior** for production
✅ **Your issue was a testing artifact**, not a bug
✅ **Solution**: Clear localStorage or use incognito when testing

The behavior you saw was:
- **Expected** ✅
- **Correct** ✅
- **Not a security issue** ✅

You just need to clear localStorage between tests when reusing the same email!
