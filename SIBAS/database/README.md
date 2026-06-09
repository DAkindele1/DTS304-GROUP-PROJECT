# SIBAS Database
**Student Information & Biometric Attendance System**
PostgreSQL Developer: Victoria Falowo

---

## Prerequisites
- PostgreSQL 18
- pgAdmin 4

## Setup

**1. Create the database**
In pgAdmin, right-click **Databases** → **Create** → **Database**, name it `sibas_db`.

**2. Open the Query Tool**
Right-click `sibas_db` → **Query Tool**

**3. Run the scripts in this order**

| Order | File | Purpose |
|---|---|---|
| 1 | `sibas_schema.sql` | Creates all tables and constraints |
| 2 | `sibas_sample_data.sql` | Inserts sample data |
| 3 | `sibas_tests.sql` | Optional — runs database tests |

For each file: open it in the Query Tool and press **F5** to run.
