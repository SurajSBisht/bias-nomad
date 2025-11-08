# Database Migration Notes

## Added `skills` field to Job model

**Date**: Current update
**Model**: `app.database.models.Job`

### Changes
- Added `skills` column to the `jobs` table
- Field type: `Text` (nullable)
- Purpose: Store required skills for job postings to improve TF-IDF recommendations

### Migration Steps

Since we're using SQLite and the field is nullable, existing databases will automatically handle the new column. However, if you have an existing database:

1. **Option 1: Let SQLAlchemy recreate tables (Development only)**
   - Delete `bias_nomad.db` file
   - Restart the server - tables will be recreated with the new schema

2. **Option 2: Manual migration (Production)**
   ```sql
   ALTER TABLE jobs ADD COLUMN skills TEXT;
   ```

### Testing
After migration, verify:
- Existing jobs have `skills = NULL` (acceptable)
- New jobs can be created with skills field
- TF-IDF recommendations work correctly with combined text fields

