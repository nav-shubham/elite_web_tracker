
# Chronos System Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

A lightweight **workout tracking and routine management system** built with FastAPI, SQLite, and Jinja2 templates. Track workouts, manage daily routines, view history, and export analytics to CSV.

---

# Table of Contents

* Introduction
* Features
* Tech Stack
* Installation
* Usage
* API Endpoints
* Database Schema
* Project Structure
* Screenshots
* Roadmap
* License

---

# Introduction

Chronos System Tracker is a personal workout tracking backend system designed to log exercises, manage routine templates, store workout history, and export analytics data. The system uses SQLite for persistent storage and FastAPI for backend APIs.

Core files:

* Database module → 
* FastAPI app → 
* Requirements → 

---

# Features

* Track exercise sets and reps
* Save routine templates per day
* Load routine templates
* View workout history
* Export workout analytics CSV
* Clear history
* SQLite database storage
* FastAPI backend
* Jinja2 frontend support
* Static file serving

---

# Tech Stack

| Technology | Purpose               |
| ---------- | --------------------- |
| FastAPI    | Backend API           |
| SQLite     | Database              |
| Jinja2     | Templates             |
| Uvicorn    | Server                |
| Pandas     | Analytics             |
| Plotly     | Visualization         |
| Streamlit  | Optional analytics UI |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/chronos-tracker.git
cd chronos-tracker
```

## Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
uvicorn main:app --reload
```

Or run:

```bash
run_app.bat
```

---

# Usage

Open browser:

```
http://127.0.0.1:8000
```

You can:

* Track workouts
* Load daily routine
* Save templates
* View history
* Export CSV analytics

---

# API Endpoints

## Track Workout

**POST** `/api/track`

```json
{
  "exercise_name": "Bench Press",
  "set_number": 1,
  "reps": 10,
  "weight": 60,
  "duration_seconds": 45
}
```

## Get Routine

**GET** `/api/routine/{day}`

## Save Routine

**POST** `/api/routine/{day}`

## Get History

**GET** `/api/history`

## Clear History

**DELETE** `/api/history`

## Export CSV

**GET** `/api/export`

---

# Database Schema

## exercise_logs

| Column           | Type     |
| ---------------- | -------- |
| id               | INTEGER  |
| log_date         | DATE     |
| exercise_name    | TEXT     |
| set_number       | INTEGER  |
| reps             | INTEGER  |
| weight           | REAL     |
| duration_seconds | INTEGER  |
| timestamp        | DATETIME |

## routine_templates

| Column        | Type    |
| ------------- | ------- |
| id            | INTEGER |
| day_name      | TEXT    |
| exercise_name | TEXT    |
| target_sets   | INTEGER |

---

# Project Structure

```
chronos-tracker/
│
├── main.py
├── database.py
├── requirements.txt
├── tracker.db
├── run_app.bat
│
├── static/
├── templates/
│
└── README.md
```

---

# Roadmap

* Add user authentication
* Add dashboard analytics
* Add exercise charts
* Add REST API documentation
* Deploy to cloud
* Mobile app integration

---

# License

MIT License

 **Deployment guide**
* **Docker setup README**
