# 🚀 Backend Architecture Overview

This document describes the foundational infrastructure of the **AI Resume Tailoring & Job Tracking Platform**. It outlines the structural decisions and system integrations required for a scalable, production-ready environment.

---

## 🎯 Purpose

This documentation serves as a guide for:
* **Future Contributors:** Understanding the "why" behind the "how."
* **Onboarding:** Getting new engineers up to speed quickly.
* **Infrastructure Debugging:** Mapping the flow of data across services.
* **Scaling:** Providing a roadmap for deployment and resource allocation.

---

## 🏗️ High-Level Architecture

The backend utilizes a modular, layered approach:
1. **Client:** Web or Mobile UI.
2. **FastAPI Application:** The entry point for all HTTP requests.
3. **Business Logic (`services/`):** Where data is processed and AI logic resides.
4. **SQLAlchemy ORM:** The bridge between Python code and raw SQL.
5. **PostgreSQL Database:** Secure, relational data storage.

> **Note:** All services are containerized using **Docker** to eliminate "works on my machine" inconsistencies.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **API Framework** | FastAPI |
| **Language** | Python 3.11 |
| **Database** | PostgreSQL 16 |
| **ORM** | SQLAlchemy |
| **Migrations** | Alembic |
| **Auth (Planned)** | JWT (JSON Web Tokens) |
| **Async Tasks** | Background Tasks / Workers |
| **Containerization** | Docker + Docker Compose |

---

## 📂 Project Structure

```text
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── core/
│   │   ├── config.py        # Centralized environment configuration
│   │   └── database.py      # SQLAlchemy engine & session management
│   ├── api/                 # HTTP route handlers (controllers)
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic layer
│   └── repositories/        # Database access layer
├── alembic/                 # Database migration system
│   ├── env.py               # Alembic runtime configuration
│   └── versions/            # Versioned migration files
├── Dockerfile               # FastAPI container definition
├── docker-compose.yml       # Multi-service orchestration
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
