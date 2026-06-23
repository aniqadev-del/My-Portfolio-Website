# SoftGemZ Website + Admin Control — PRD

## Original Problem Statement
Professional website for SoftGemZ software house (AI & Automation solutions) with a functional
contact form + DB integration, plus a comprehensive Admin Control at `/admin` with predefined
credentials. Admin features: view/filter/search/export contact submissions, respond to messages
(DB-tracked + real email via Gmail SMTP), manage Portfolio & Services content dynamically,
a statistics dashboard, and desktop image upload for portfolio projects.

## Tech Stack
- Frontend: React, Tailwind, Recharts, Context API, Axios
- Backend: FastAPI, Motor (async MongoDB), PyJWT, smtplib, Cloudinary SDK
- DB: MongoDB Atlas (DB_NAME=softgemz_database)
- Integrations: MongoDB Atlas, Gmail SMTP, Cloudinary

## Architecture
- backend/server.py — all routes, JWT auth, SMTP, Cloudinary
- backend/migrate_mock_data.py — seeds portfolio (5) + services (4)
- frontend/src/contexts/AdminContext.jsx — admin auth state
- frontend/src/pages/admin/*.jsx — admin UI (Layout, Login, Dashboard, Contacts, Portfolio, Services)
- frontend/src/pages/Portfolio.jsx & Services.jsx — public pages fetch from DB

## Key Endpoints
- POST /api/admin/login
- GET/PUT /api/admin/contacts, POST /api/admin/contacts/{id}/respond, GET .../export
- GET/POST/PUT/DELETE /api/admin/portfolio and /api/admin/services
- POST /api/admin/upload-image (Cloudinary)
- GET /api/portfolio, GET /api/services (public)
- GET /api/admin/stats

## Status / Changelog
- 2026-06-23: RESOLVED outage. MongoDB Atlas cluster (cluster0.flhyyxv) was paused/unreachable
  causing dashboard load failure + image-upload save failures. User provided new cluster
  (cluster0.t2chdb7). Updated MONGO_URL, re-ran migration (5 portfolio, 4 services restored).
  Verified: dashboard stats, public portfolio/services, Cloudinary upload all working.
- Prior: Admin panel fully built — auth, dashboard, contacts CRUD+CSV+email, Portfolio/Services CRUD,
  Cloudinary upload for Portfolio.

## Backlog / Next Tasks
- P1: Add Cloudinary desktop image upload to Services section (parity with Portfolio) — AdminServices.jsx + server.py
- P2: Email validation rejects consecutive dots (test..test@example.com currently accepted)
- P2: Auth middleware returns 403 instead of 401 for missing token
- P3: Refactor server.py into routers/models/utils modules
