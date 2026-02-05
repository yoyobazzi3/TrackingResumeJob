## 🚀 Backend Architecture OverviewThis document describes the foundational infrastructure of the AI Resume Tailoring & Job Tracking Platform. It outlines the structural decisions and system integrations required for a scalable, production-ready environment.## 🎯 PurposeThis documentation serves as a guide for:Future Contributors: Understanding the "why" behind the "how."Onboarding: Getting new engineers up to speed quickly.Infrastructure Debugging: Mapping the flow of data across services.Scaling: Providing a roadmap for deployment and resource allocation.## 🏗️ High-Level ArchitectureThe backend utilizes a modular, layered approach:Client: Web or Mobile UI.FastAPI Application: The entry point for all HTTP requests.Business Logic (services/): Where data is processed and AI logic resides.SQLAlchemy ORM: The bridge between Python code and raw SQL.PostgreSQL Database: Secure, relational data storage.Note: All services are containerized using Docker to eliminate "works on my machine" inconsistencies.## 🛠️ Technology StackComponentTechnologyAPI FrameworkFastAPILanguagePython 3.11DatabasePostgreSQL 16ORMSQLAlchemyMigrationsAlembicAuth (Planned)JWT (JSON Web Tokens)Async TasksBackground Tasks / WorkersContainerizationDocker + Docker Compose## 📂 Project StructurePlaintextbackend/
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
## 🐳 Docker & Containerization### Why Docker?Consistency: Identical runtimes across dev, CI, and production.Isolation: Dependencies for the API don't conflict with the host system.Scalability: Effortless addition of async workers or cache layers.### Service ConfigurationAPI Service (resume_api)Uses Uvicorn for the ASGI server. The source code is bind-mounted to allow for real-time development updates without rebuilding the image.YAMLvolumes:
  - .:/app
Database Service (resume_db)Runs PostgreSQL 16. Uses a named volume to ensure data persists even if the container is destroyed or updated.YAMLvolumes:
  - postgres_data:/var/lib/postgresql/data
## 🔐 Configuration & Database Layer### Centralized SettingsWe use pydantic-settings in app/core/config.py to manage environment variables. This ensures:A single source of truth for configuration.Validation of critical variables (like DATABASE_URL) at startup.Security by preventing hardcoded credentials in the codebase.### Database Migrations (Alembic)Alembic manages schema changes safely. The alembic/env.py file bridges the gap between:SQLAlchemy Models: The source of truth for the schema.Database Connection: Provided via the Pydantic settings.Migration Engine: To autogenerate and apply changes transactionally.## 📌 Key Architectural RulesRule of Thumb:Code is mounted (via bind mounts for instant updates).Data is volumed (via named volumes for persistence).