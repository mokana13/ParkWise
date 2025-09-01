# Vehicle Parking System - V2

A full-stack Vehicle Parking Management Web App with **Flask** (Backend API), **Vue.js** (Frontend), **SQLite**, **Redis**, and **Celery** for managing parking lots and user reservations.

---

## Tech Stack

- **Frontend**: Vue.js 2 + Bootstrap
- **Backend**: Flask (Python) REST API
- **Database**: SQLite
- **Background Jobs**: Celery + Redis
- **Async Tasks**: Email/SMS Reminders, Monthly Reports, Auto-Release
- **Auth**: Flask-Login with Admin & User Roles

---

## Features

### User
- Register and Login
- View available parking lots & spots
- Reserve and release a parking spot
- View reservation history

### Admin
- Predefined login (no registration)
- Dashboard view with welcome message and role
- Add/Edit/Delete Parking Lots
- View parking spot details
- View all registered users

---

## How to Run (on Windows)

### 1. Clone the Project
git clone https://github.com/your-username/vehicle-parking-system.git
cd vehicle-parking-system

### 2. Set Up Python Virtual Environment
Install Python (Skip if already installed)
Download from https://www.python.org/downloads/windows/

Create Virtual Environment

python -m venv venv
venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt
Run Flask API

set FLASK_APP=app.py
set FLASK_ENV=development
flask run
3. Setup Redis (on Windows)
Install Redis via Memurai (Redis for Windows)
OR

Use Redis via Docker

Start Redis server before using Celery.

4. Setup Celery (Background Jobs)

venv\Scripts\activate
celery -A tasks.celery worker --loglevel=info
5. Setup Vue Frontend
Install Node.js (Skip if already installed)
Download from https://nodejs.org/


cd frontend
npm install
npm run dev
Frontend runs at: http://localhost:5173

 Project Highlights
 Email/SMS Reminders (via Celery jobs)

 Daily tasks to remind users to book/release

 Monthly report generation for parking usage

 Aesthetic sidebar dashboards for Admin and User

 Role-based access (Admin vs User)

 Easy setup on any Windows system#
