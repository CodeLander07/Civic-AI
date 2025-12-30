# Technical Decisions Log

## 2025-12-29: Authentication & Security

### 1. Supabase Row Level Security (RLS) Bypass for User Creation
**Context:**
During user signup, the backend attempts to insert a new row into the `users` table. This failed with "new row violates row-level security policy" because the operation was performed using the anonymous (public) key.

**Decision:**
We implemented a server-side administrative client using the `SUPABASE_SERVICE_ROLE_KEY`.

**Implementation:**
- Added `SUPABASE_SERVICE_ROLE_KEY` to `.env`.
- Initialized `supabase_admin` client in `server/main.py`.
- Updated the `/auth/signup` endpoint to use `supabase_admin` for inserting user profiles.

### 2. Auto-Confirmation of Emails (Hackathon Mode)
**Context:**
Supabase Auth defaults to requiring email verification. This causes friction during hackathon demos.

**Decision:**
We enabled an "Auto-Confirm" mechanism for new signups.

**Implementation:**
- In `server/main.py`, immediately after a successful signup, the backend uses the `supabase_admin` client to update the user's status to `email_confirm: True`.
- If the session is not returned immediately, the backend performs a login on behalf of the user.

## 2025-12-30: Frontend & Build

### 3. TypeScript JSX Namespace Fix
**Context:**
The Next.js build failed with `Cannot find namespace 'JSX'` in `client/components/dashboard/ChatMessage.tsx`.

**Decision:**
Standardize on `React.ReactNode` instead of global `JSX` namespace.

**Implementation:**
- Imported `React` in the component file.
- Changed type annotation from `JSX.Element[]` to `React.ReactNode[]`.

## 2025-12-30: Backend Dependencies

### 4. Resolution of `httpx` Version Conflicts
**Context:**
`pip install` failed because `supabase` requires `httpx<0.28` while other packages requested newer versions.

**Decision:**
Pin `httpx` to a compatible range that satisfies all dependencies.

**Implementation:**
- Updated `server/requirements.txt` to specify `httpx>=0.27.0,<0.28.0`.

## 2025-12-31: Architecture

### 5. Reversion to Monolithic Backend
**Context:**
We attempted to refactor `server/main.py` into a modular structure (`api/`, `services/`, `models/`) to improve maintainability. However, this introduced complexity and potential breakage during the critical hackathon phase.

**Decision:**
Revert to a monolithic `main.py` structure.

**Reasoning:**
- **Velocity:** A single file is easier to debug and modify quickly during a hackathon.
- **Simplicity:** Reduces import errors and circular dependencies.
- **Focus:** Allows the team to focus on features (Fallbacks, AI prompts) rather than architectural purity.

**Implementation:**
- Restored `server/main.py` as the single source of truth.
- Kept `server/fallbacks.py` as a separate module for data isolation.
