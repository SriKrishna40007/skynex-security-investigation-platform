# Architecture Overview

**Product:** SKYNEX

**Version:** 1.0

**Status:** Approved

---

# Introduction

SKYNEX is an AI-Powered Cloud Security Investigation Platform built as a modern SaaS application using a modular, secure, and scalable architecture.

The platform is designed using separation of concerns, clean architecture principles, and secure-by-design engineering practices.

---

# High-Level Architecture

```
                   Internet
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
  Public Website              SaaS Application
         │                           │
         └─────────────┬─────────────┘
                       ▼
               Next.js Frontend
                       │
               HTTPS / REST API
                       │
                       ▼
              FastAPI Backend
                       │
      ┌────────────────┼────────────────┐
      │                │                │
      ▼                ▼                ▼
 Authentication   Business Logic   Security Engines
      │                │                │
      └────────────────┼────────────────┘
                       ▼
                 PostgreSQL Database
```

---

# Technology Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui

---

## Backend

- FastAPI
- Python
- SQLAlchemy
- Alembic

---

## Database

- PostgreSQL

---

## Infrastructure

- Docker
- Docker Compose
- GitHub Actions

---

# Core Modules

## Public Website

Responsible for:

- Marketing pages
- Product information
- Documentation
- User onboarding

---

## Authentication

Responsible for:

- User registration
- Login
- JWT authentication
- RBAC

---

## Dashboard

Responsible for:

- Security overview
- Risk summaries
- Investigation metrics

---

## Investigation Center

Responsible for:

- Managing investigations
- Tracking findings
- Correlation workflows
- Investigation history

---

## AI Investigation Engine

Responsible for:

- AI summaries
- Root cause analysis
- Technical recommendations
- Business impact analysis

---

## Reporting

Responsible for:

- Executive reports
- Technical reports
- Investigation exports

---

## Administration

Responsible for:

- Organizations
- Users
- Roles
- Audit logs
- Platform settings

---

# Architectural Principles

SKYNEX follows these principles:

- Modular Design
- Clean Architecture
- Separation of Concerns
- Secure by Design
- API First
- Stateless Services
- Scalability
- Maintainability
- Testability

---

# Security Principles

Every architectural component must support:

- Authentication
- Authorization
- Audit Logging
- Secure Communication
- Input Validation
- Least Privilege
- Secret Management

---

# Future Expansion

The architecture supports future additions such as:

- Multi-cloud integrations
- AI agents
- Knowledge graph
- Attack path visualization
- Compliance automation
- Multi-tenancy enhancements
