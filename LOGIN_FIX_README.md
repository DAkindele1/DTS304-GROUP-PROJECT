# SIBAS Login Issue - Root Cause & Fix

## Problem Summary

❌ **Issue Reported**: Users cannot login with credentials from the database.
- Error: `System Error encountered: Invalid salt`
- Cause: Password verification mismatch between database storage and authentication code

---

## Root Cause Analysis

### What Was Happening:
1. **Database Schema** (`sibas_schema.sql`): `password` column stores plain text
2. **Sample Data** (`sibas_sample_data.sql`): Had placeholder text like `'hashed_password_001'` (not actual hashes)
3. **Authentication Code** (`authentication.py`): Expects bcrypt hashes and tries to verify with `bcrypt.checkpw()`
4. **Result**: Trying to verify plain text against bcrypt → `Invalid salt` error

### The Mismatch:
```python
# Code tries to do this:
verify_password("password123", "hashed_password_001")
    ↓
bcrypt.checkpw(password.encode(), hash.encode())
    ↓
# But "hashed_password_001" is NOT a valid bcrypt hash!
# Bcrypt hashes look like: $2b$12$pwGv8oCpP.b3pM2gThlP2uZn7OTm1hvXCMvNkF9W3XuXUEYOfS47O
```

---

## Solution: Replace Sample Data with Hashed Passwords

### Step 1: Backup Old Data
```bash
# Your current sample data file:
sibas_sample_data.sql  (OLD - has plain text passwords)
```

### Step 2: Use New Hashed Sample Data
```bash
# New file with proper bcrypt hashes:
sibas_sample_data_hashed.sql
```

### Step 3: Clear & Reload Database

If you have an existing database with bad data:

```sql
-- DANGER: Only run if you want to clear all data
-- Disable foreign key checks
ALTER TABLE users DISABLE TRIGGER ALL;
DELETE FROM users;
DELETE FROM roles;
ALTER TABLE users ENABLE TRIGGER ALL;

-- Then reload:
-- 1. sibas_schema.sql
-- 2. sibas_indexes.sql
-- 3. sibas_sample_data_hashed.sql (use this one!)
```

---

## Test Credentials

### Admin Account
- **Username**: `admin_ford_pines`
- **Password**: `admin_password`
- **Role**: Administrator

### Lecturer Account
- **Username**: `lec_eda_clawthorne`
- **Password**: `lecturer_password`
- **Role**: Lecturer

### Student Account
- **Username**: `stu_marinette_dupain`
- **Password**: `student_password`
- **Role**: Student

---

## Password Hashing Information

All passwords have been hashed using bcrypt with:
- Algorithm: bcrypt (cost factor: 12)
- Format: `$2b$12$` + 53 character hash

**Hashes Generated:**
- `admin_password` → `$2b$12$pwGv8oCpP.b3pM2gThlP2uZn7OTm1hvXCMvNkF9W3XuXUEYOfS47O`
- `lecturer_password` → `$2b$12$qnCjOyXPZEu0F2z4iydjJujWWXa4pkoYkMjkJc.YfUZpqQUnVrF.2`
- `student_password` → `$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m`

### To Regenerate Hashes

If you want to create new passwords, use the provided script:

```bash
python generate_bcrypt_hashes.py
```

This will output SQL INSERT statements with actual bcrypt hashes.

---

## Verify Login Works

### Manual Test in Database

```sql
-- Test: Verify a user exists with bcrypt hash
SELECT user_id, username, password, role_id 
FROM users 
WHERE username = 'admin_ford_pines';
```

Expected output:
```
user_id | username          | password (bcrypt hash)                         | role_id
--------|-------------------|------------------------------------------------|--------
    1   | admin_ford_pines  | $2b$12$pwGv8oCpP.b3pM2gThlP2uZn7OTm1hvX...   |   1
```

### App Test

1. Start Streamlit app:
   ```bash
   streamlit run SIBAS/app/main.py
   ```

2. Go to `http://localhost:8501`

3. Try login with credentials above

4. Should see: `Access Granted. Redirecting to landing portal...` ✅

---

## Code Notes

The authentication code in `authentication.py` is **correct**:

```python
def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against an existing bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
```

The issue was **data**, not code. The database had incorrect password format.

---

## Files Provided

| File | Purpose |
|------|---------|
| `sibas_sample_data_hashed.sql` | **USE THIS** - Sample data with proper bcrypt hashes |
| `generate_bcrypt_hashes.py` | Utility to generate new bcrypt hashes for custom passwords |

---

## Summary

✅ **What Changed**: Sample data passwords now use actual bcrypt hashes  
✅ **What Stays Same**: Authentication code unchanged (already correct)  
✅ **What to Do**: Replace old sample data with the hashed version  
✅ **Result**: Logins will work with provided test credentials
