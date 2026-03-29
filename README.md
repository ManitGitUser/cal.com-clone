# Scheduling Platform (Cal.com Clone)

## Overview

This project is a simplified scheduling and booking platform inspired by Cal.com. It allows users to create event types, define availability, and enable others to book time slots.

## Features

* Event type creation (title, duration, slug)
* Availability setup (days and time slots)
* Public booking page
* Time slot selection
* Booking with name and email
* Prevention of double booking
* View and cancel bookings

## Tech Stack

* Backend: FastAPI (Python)
* Frontend: React.js
* Database: PostgreSQL / SQLite
* Deployment: Render (Backend), Vercel (Frontend)

## Database Design

### EventType

* id
* title
* description
* duration
* slug

### Availability

* id
* event_id (FK)
* day_of_week
* start_time
* end_time

### Booking

* id
* event_id (FK)
* name
* email
* start_time
* end_time

Constraints:

* Unique (event_id, start_time) to prevent double booking

## API Endpoints

* POST /events
* GET /events
* POST /availability
* GET /slots
* POST /book
* GET /bookings
* DELETE /booking/{id}

## Setup Instructions

### Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
npm install
npm start
```

## Assumptions

* Single user (no authentication required)
* Fixed timezone handling
* Minimal UI due to time constraints

## Future Improvements

* Authentication system
* Email notifications
* Rescheduling feature
* Advanced timezone handling
* Better UI/UX
