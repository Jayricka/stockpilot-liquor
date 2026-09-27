# StockPilot Liquor

**StockPilot Liquor** is a modern inventory, sales, and business management platform designed for licensed liquor retailers in Kenya.

It helps liquor-store owners manage products, stock, purchases, sales, suppliers, deliveries, and business performance from one centralized system.

> **Project status:** Core backend MVP completed, backend test suite standardized with **133 tests passing**, and frontend architecture refactored using custom React hooks, focused components, and a dedicated service layer.
>
> **Next milestone:** Billing plan entitlements, Daraja/M-Pesa integration, production configuration, and deployment.

---

## Table of Contents

* [Overview](#overview)
* [Core Features](#core-features)
* [Technology Stack](#technology-stack)
* [Architecture](#architecture)
* [Project Structure](#project-structure)
* [Backend Modules](#backend-modules)
* [Frontend Architecture](#frontend-architecture)
* [Installation](#installation)
* [Environment Configuration](#environment-configuration)
* [Running the Project](#running-the-project)
* [Testing](#testing)
* [Automation Scripts](#automation-scripts)
* [API Overview](#api-overview)
* [Business Data Isolation](#business-data-isolation)
* [Development Workflow](#development-workflow)
* [Git Branches](#git-branches)
* [Roadmap](#roadmap)
* [Security Notes](#security-notes)
* [Compliance Considerations](#compliance-considerations)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

Liquor retailers often rely on manual stock records, spreadsheets, notebooks, and disconnected tools. This makes it difficult to track stock levels, calculate profits, manage suppliers, and understand daily business performance.

StockPilot Liquor is being developed to solve these challenges through a simple, scalable, and mobile-friendly SaaS platform.

### Main Objectives

* Reduce stock losses and inventory errors.
* Prevent sales of unavailable products.
* Track purchases and supplier relationships.
* Monitor revenue, costs, and gross profit.
* Support multiple businesses with strict data isolation.
* Provide subscription-based access through configurable plans and entitlements.
* Provide a foundation for M-Pesa and future payment integrations.
* Provide a foundation for future eTIMS integration.
* Offer a professional platform that can be licensed to liquor retailers in Kenya.

---

## Core Features

### Authentication

* Email-based user authentication.
* User registration.
* Login and logout.
* JWT access and refresh tokens.
* Protected API endpoints.
* Custom user model.

### Business Management

* Create and manage businesses.
* Business membership system.
* Business roles:

  * Owner
  * Manager
  * Staff
* Active and inactive memberships.
* Business-level data isolation.
* Authenticated business selection.

### Products and Categories

* Create product categories.
* Create, update, list, and retrieve products.
* Product SKU management.
* Product units:

  * Bottle
  * Litre
  * Crate
  * Piece
* Buying and selling prices.
* Current stock quantity.
* Reorder levels.
* Low-stock detection.
* Product ownership validation.
* Business-scoped product and category access.

### Inventory

* Stock increases through completed purchases.
* Stock decreases through completed sales.
* Stock movement history.
* Purchase, sale, adjustment, and return movement types.
* Overselling prevention.
* Stock balance tracking.
* Business and product ownership checks.

### Purchases

* Create purchase records.
* Add multiple products to a purchase.
* Track suppliers.
* Calculate purchase totals.
* Complete purchases.
* Increase stock after purchase completion.
* Cancel draft purchases.
* Prevent invalid purchase transitions.

### Sales

* Create sales with multiple products.
* Invoice number tracking.
* Payment methods:

  * Cash
  * M-Pesa
  * Card
  * Credit
* Discount support.
* Stock availability checks.
* Automatic stock deduction.
* Buying and selling price snapshots.
* Revenue calculation.
* Cost calculation.
* Gross profit calculation.
* Sale completion and cancellation workflows.

### Suppliers

* Create and manage suppliers.
* Supplier contact information.
* Supplier addresses and notes.
* Business-specific supplier records.
* Duplicate supplier prevention.

### Deliveries

* Create delivery orders for completed sales.
* Customer name and phone.
* Delivery address.
* Delivery fee.
* Assign delivery staff.
* Delivery status tracking:

  * Pending
  * Assigned
  * Out for delivery
  * Delivered
  * Cancelled
* Delivery transition validation.

### Reports and Dashboard

* Today's sales count.
* Today's revenue.
* Today's gross profit.
* Active product count.
* Low-stock product count.
* Total stock value.
* Pending deliveries.
* Sales by payment method.
* Top-selling products.
* Low-stock products.
* Recent sales.
* Recent purchases.

### Billing and Subscriptions

The billing foundation is implemented and is being prepared for entitlement enforcement.

Planned entitlement capabilities include:

* Subscription plans.
* Plan-specific feature access.
* Plan-specific usage limits.
* Trial support.
* Subscription status handling.
* Backend entitlement enforcement.
* Frontend entitlement-aware UI.
* Subscription lifecycle management.

Detailed entitlement rules will be implemented as the next development milestone.

### Payments

Payment integration is planned around the Kenyan payment ecosystem.

The upcoming payment milestone will include:

* Daraja API integration.
* M-Pesa payment initiation.
* M-Pesa callback handling.
* Payment verification.
* Payment transaction records.
* Subscription activation after successful payment.
* Subscription renewal handling.
* Payment failure handling.
* Idempotent payment processing.

---

## Technology Stack

### Backend

* Python
* Django
* Django REST Framework
* Simple JWT
* SQLite for local development
* PostgreSQL planned for production
* Django CORS Headers

### Frontend

* React
* Vite
* Tailwind CSS v4
* React Router
* Axios
* Lucide React
* Recharts
* Responsive SaaS dashboard interface
* Light and dark theme support
* Custom React hooks
* Component-based workspace architecture

### Development Tools

* Git
* GitHub
* Postman or Insomnia
* Docker
* Render or another cloud platform
* Bash automation scripts
* Yarn

---

## Architecture

StockPilot follows a layered architecture designed to keep application responsibilities separated.

### Backend Flow

```text
API Request
    ↓
Django REST Framework View
    ↓
Serializer / Validation
    ↓
Service Layer
    ↓
Models / Database
```

Business-sensitive operations use explicit business and membership checks to maintain tenant isolation.

### Frontend Flow

```text
Page
    ↓
Custom Hook
    ↓
Service Layer
    ↓
API
    ↓
Django Backend
```

This keeps UI components focused on presentation while hooks handle state and workspace logic and services handle API communication.

### Overall Application Flow

```text
React Frontend
      ↓
Custom Hooks
      ↓
Frontend Services
      ↓
Django REST API
      ↓
API Views
      ↓
Backend Services
      ↓
Database
```

---

## Project Structure

```text
stockpilot-liquor/
├── README.md
├── .gitignore
├── LICENSE
├── scripts/
│   ├── migrate.sh
│   ├── push.sh
│   ├── setup.sh
│   ├── start.sh
│   └── test.sh
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── accounts/
│   │   └── tests/
│   │
│   ├── businesses/
│   │   └── tests/
│   │
│   ├── products/
│   │   └── tests/
│   │
│   ├── inventory/
│   │   └── tests/
│   │
│   ├── sales/
│   │   └── tests/
│   │
│   ├── suppliers/
│   │   └── tests/
│   │
│   ├── deliveries/
│   │   └── tests/
│   │
│   ├── reports/
│   │   └── tests/
│   │
│   ├── billing/
│   │   └── tests/
│   │
│   └── demo/
│       └── tests/
│
└── frontend/
    ├── package.json
    ├── yarn.lock
    ├── vite.config.js
    ├── index.html
    ├── .env.example
    │
    └── src/
        ├── App.jsx
        ├── App.css
        ├── index.css
        ├── main.jsx
        │
        ├── context/
        │   ├── ThemeContext.jsx
        │   ├── AuthContext.jsx
        │   └── BusinessContext.jsx
        │
        ├── data/
        │   └── landingPage.js
        │
        ├── services/
        │   ├── api.js
        │   ├── auth.js
        │   ├── dashboard.js
        │   ├── products.js
        │   └── ...
        │
        ├── pages/
        │   ├── auth/
        │   ├── dashboard/
        │   ├── products/
        │   └── ...
        │
        ├── components/
        │   ├── Navbar.jsx
        │   ├── Hero.jsx
        │   ├── DashboardPreview.jsx
        │   ├── Features.jsx
        │   ├── WhyStockPilot.jsx
        │   ├── HowItWorks.jsx
        │   ├── Pricing.jsx
        │   ├── FAQ.jsx
        │   ├── ContactCTA.jsx
        │   ├── Footer.jsx
        │   │
        │   ├── layout/
        │   │   ├── AppLayout.jsx
        │   │   ├── Sidebar.jsx
        │   │   └── Topbar.jsx
        │   │
        │   ├── dashboard/
        │   ├── products/
        │   └── ...
        │
        └── styles/
            ├── layout.css
            ├── navbar.css
            ├── hero.css
            ├── dashboard.css
            ├── dashboard-cards.css
            ├── dashboard-tables.css
            ├── sections.css
            ├── responsive.css
            ├── auth.css
            ├── app-layout.css
            └── saas-dashboard.css
```

---

## Backend Modules

### Accounts

Responsible for:

* User registration.
* Authentication.
* JWT tokens.
* User profile management.
* User access control.

### Businesses

Responsible for:

* Business creation.
* Business ownership.
* Business memberships.
* Business roles.
* Business-level isolation.

### Products

Responsible for:

* Product management.
* Category management.
* Product classification.
* Pricing.
* Product availability.

### Inventory

Responsible for:

* Stock balances.
* Stock movements.
* Inventory adjustments.
* Stock validation.

### Purchases

Responsible for:

* Purchase records.
* Purchase items.
* Supplier relationships.
* Purchase completion.
* Stock increases.

### Sales

Responsible for:

* Sales.
* Sale items.
* Payment methods.
* Stock validation.
* Sale completion.
* Sale cancellation.
* Revenue and gross profit calculations.

### Suppliers

Responsible for:

* Supplier records.
* Supplier contact information.
* Business-specific supplier management.

### Deliveries

Responsible for:

* Delivery orders.
* Delivery assignments.
* Delivery status transitions.
* Customer delivery information.

### Reports

Responsible for:

* Sales summaries.
* Revenue.
* Gross profit.
* Product performance.
* Stock insights.
* Dashboard metrics.

### Billing

Responsible for:

* Subscription records.
* Plans.
* Billing state.
* Trial state.
* Subscription lifecycle.
* Future entitlement enforcement.

---

## Frontend Architecture

The frontend is progressively structured around focused pages, components, hooks, and services.

### Page Responsibilities

Pages primarily coordinate:

* Workspace state.
* Custom hooks.
* Components.
* User interactions.

### Hook Responsibilities

Custom hooks encapsulate:

* Workspace state.
* API loading.
* Form state.
* Filtering.
* Validation.
* Business selection.
* Workspace actions.

Examples:

```text
useProductWorkspace
useProductFilters
useProductForm
useCategoryForm
```

### Component Responsibilities

Components focus on individual UI responsibilities rather than combining an entire workspace into one large file.

For example, the Products workspace separates:

```text
Products
├── ProductHeader
├── ProductStats
├── ProductFilters
├── ProductTable
├── ProductRow
├── ProductLoading
├── ProductEmptyState
└── ProductForm
    ├── ProductClassification
    ├── ProductFormFields
    ├── ProductPricing
    ├── ProductInventory
    └── ProductStatus
```

This pattern provides a foundation for progressively refactoring the remaining workspaces.

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd stockpilot-liquor
```

### Backend Setup

```bash
cd backend

python3 -m venv myenv
source myenv/bin/activate

pip install -r requirements.txt

python manage.py migrate
```

### Frontend Setup

```bash
cd ../frontend

yarn install
```

---

## Environment Configuration

### Backend

Create:

```text
backend/.env
```

Use the example configuration as a starting point:

```text
backend/.env.example
```

Production configuration should use secure environment variables for:

* Django secret key.
* Database credentials.
* Allowed hosts.
* CORS configuration.
* JWT configuration.
* Daraja credentials.
* Payment callback configuration.
* Other third-party service credentials.

### Frontend

Create:

```text
frontend/.env
```

based on:

```text
frontend/.env.example
```

Do not commit environment files containing secrets.

---

## Running the Project

### Start Backend

```bash
cd backend

source myenv/bin/activate

python manage.py runserver
```

The development API will be available through:

```text
http://127.0.0.1:8000/
```

### Start Frontend

In another terminal:

```bash
cd frontend

yarn dev
```

The Vite development server will provide the frontend URL in the terminal.

---

## Testing

The backend test suite has been fully standardized into focused test modules.

### Run All Backend Tests

```bash
cd backend

python manage.py test
```

Current validation:

```text
Ran 133 tests in 157.051s

OK
```

### Test Organization

Backend tests are organized by application and responsibility rather than maintaining large monolithic test files.

Examples include:

```text
accounts/tests/
businesses/tests/
products/tests/
inventory/tests/
sales/tests/
suppliers/tests/
deliveries/tests/
reports/tests/
billing/tests/
demo/tests/
```

The standardized structure makes it easier to:

* Locate specific tests.
* Add new test cases.
* Debug failures.
* Reuse common setup.
* Maintain business isolation coverage.
* Maintain API and service-layer coverage.

### Frontend Validation

Run:

```bash
yarn lint
yarn build
```

Both commands should complete successfully before merging frontend changes.

---

## Automation Scripts

The project contains Bash scripts to simplify common development tasks.

```text
scripts/
├── migrate.sh
├── push.sh
├── setup.sh
├── start.sh
└── test.sh
```

These scripts are intended to reduce repetitive development commands and provide a consistent local workflow.

---

## API Overview

The API is organized around authenticated business resources.

### Authentication

```text
/api/auth/
```

Examples:

```text
POST /api/auth/register/
POST /api/auth/login/
GET  /api/auth/me/
```

### Businesses

```text
/api/businesses/
```

### Products

```text
/api/businesses/<business_id>/products/
```

### Categories

```text
/api/businesses/<business_id>/categories/
```

### Inventory

```text
/api/
```

### Sales

```text
/api/
```

### Deliveries

```text
/api/
```

### Reports

```text
/api/
```

### Billing

```text
/api/billing/
```

The API is protected through authentication and business-level access controls.

---

## Business Data Isolation

StockPilot is designed as a multi-business SaaS application.

Business-owned resources must be accessed within the context of an authenticated user's active business membership.

The backend validates:

* Authenticated user identity.
* Business membership.
* Active membership status.
* Business ownership.
* Resource ownership.
* Related object ownership.

Business-scoped endpoints reject requests where the authenticated user does not have access to the requested business.

This provides the foundation for secure multi-tenant operation.

---

## Development Workflow

Development follows a structured workflow focused on maintainability and controlled changes.

### Feature Workflow

```text
Plan
  ↓
Design
  ↓
Implement
  ↓
Test
  ↓
Refactor
  ↓
Lint / Build
  ↓
Commit
  ↓
Push
  ↓
Pull Request
  ↓
Review
  ↓
Merge
  ↓
Pull Main
```

### Refactoring Principles

The project follows these principles:

* Keep files focused.
* Separate responsibilities.
* Prefer reusable hooks over duplicated state logic.
* Keep API calls in service modules.
* Keep business logic in backend services.
* Use transactions for critical state changes.
* Maintain automated test coverage.
* Avoid unrelated changes.
* Validate before merging.

---

## Git Branches

The project uses Git branches to isolate development work.

Typical workflow:

```bash
git checkout main
git pull origin main

git checkout -b feature/<feature-name>
```

After implementation:

```bash
git status
git add .
git commit -m "<commit message>"
git push origin <branch-name>
```

Create a Pull Request against `main`.

After the Pull Request is merged:

```bash
git checkout main
git pull origin main
```

---

## Roadmap

### Completed

* [x] Django backend foundation
* [x] Custom user authentication
* [x] JWT authentication
* [x] Business management
* [x] Business memberships
* [x] Business roles
* [x] Business data isolation
* [x] Product management
* [x] Category management
* [x] Inventory management
* [x] Purchase workflows
* [x] Sales workflows
* [x] Supplier management
* [x] Delivery management
* [x] Reports and dashboard
* [x] Billing foundation
* [x] Frontend authentication flow
* [x] Frontend business dashboard
* [x] Frontend Products workspace
* [x] Custom React hooks
* [x] Frontend componentization
* [x] Frontend service-layer organization
* [x] Backend unit-test standardization
* [x] 133 backend tests passing

### In Progress

* [ ] Billing plan entitlements
* [ ] Entitlement enforcement
* [ ] Subscription-aware frontend controls

### Next

* [ ] Daraja API integration
* [ ] M-Pesa payment initiation
* [ ] M-Pesa callback processing
* [ ] Payment verification
* [ ] Payment-to-subscription workflow
* [ ] Subscription renewal workflow
* [ ] Payment failure handling
* [ ] Idempotent payment processing

### Production

* [ ] PostgreSQL production database
* [ ] Production environment configuration
* [ ] Secure secrets management
* [ ] Production CORS configuration
* [ ] Production API configuration
* [ ] Frontend production build
* [ ] Backend deployment
* [ ] Frontend deployment
* [ ] Domain configuration
* [ ] HTTPS verification
* [ ] Production monitoring
* [ ] End-to-end production testing

### Future

* [ ] eTIMS integration
* [ ] Advanced analytics
* [ ] Automated business reports
* [ ] Customer management
* [ ] Expense tracking
* [ ] Advanced supplier management
* [ ] Mobile/PWA improvements
* [ ] Additional business categories

---

## Security Notes

StockPilot handles business and financial data and therefore requires secure handling of authentication and tenant data.

### Current Security Measures

* JWT authentication.
* Protected API endpoints.
* Authenticated business access.
* Active membership validation.
* Business-scoped queries.
* Resource ownership validation.
* Stock ownership validation.
* Protected environment configuration.
* Transactional service operations where required.

### Production Requirements

Before production deployment:

* Use PostgreSQL.
* Use HTTPS.
* Rotate development secrets.
* Store secrets exclusively in environment variables or a secure secrets manager.
* Configure production `ALLOWED_HOSTS`.
* Configure production CORS.
* Disable Django debug mode.
* Secure JWT configuration.
* Secure Daraja credentials.
* Protect payment callbacks.
* Add appropriate logging and monitoring.
* Review authorization across every business-scoped endpoint.

---

## Compliance Considerations

StockPilot is intended for the Kenyan market and may eventually integrate with services and systems subject to local regulatory requirements.

Potential future integrations include:

* M-Pesa through Safaricom Daraja.
* eTIMS.
* Other payment and financial services.

Compliance requirements should be reviewed and validated before enabling production integrations.

StockPilot does not replace professional legal, tax, accounting, or regulatory advice.

---

## Contributing

Contributions should follow the project's development standards.

Before submitting changes:

1. Keep changes focused.
2. Follow the existing architecture.
3. Add or update tests where applicable.
4. Run the backend test suite.
5. Run frontend linting.
6. Run the frontend production build.
7. Create a descriptive commit.
8. Open a Pull Request.
9. Address review feedback.
10. Merge only after validation.

---

## License

This project is licensed under the terms specified in the `LICENSE` file.

