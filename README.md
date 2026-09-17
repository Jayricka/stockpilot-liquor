# StockPilot Liquor

**StockPilot Liquor** is a modern inventory, sales, and business management platform designed for licensed liquor retailers in Kenya.

It helps liquor-store owners manage products, stock, purchases, sales, suppliers, deliveries, and business performance from one centralized system.

> **Project status:** Backend MVP completed and tested — **79 tests passing**.
> Frontend MVP implemented with a professional landing page, authentication flow, and API-connected business dashboard.

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Backend Modules](#backend-modules)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Automation Scripts](#automation-scripts)
- [API Overview](#api-overview)
- [Business Data Isolation](#business-data-isolation)
- [Development Workflow](#development-workflow)
- [Git Branches](#git-branches)
- [Roadmap](#roadmap)
- [Security Notes](#security-notes)
- [Compliance Considerations](#compliance-considerations)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Liquor retailers often rely on manual stock records, spreadsheets, notebooks, and disconnected tools. This makes it difficult to track stock levels, calculate profits, manage suppliers, and understand daily business performance.

StockPilot Liquor is being developed to solve these challenges through a simple, scalable, and mobile-friendly SaaS platform.

### Main Objectives

- Reduce stock losses and inventory errors.
- Prevent sales of unavailable products.
- Track purchases and supplier relationships.
- Monitor revenue, costs, and gross profit.
- Support multiple businesses with strict data isolation.
- Provide a foundation for future M-Pesa and eTIMS integrations.
- Offer a professional platform that can be licensed to liquor retailers.

---

## Core Features

### Authentication

- Email-based user authentication.
- User registration.
- Login and logout.
- JWT access and refresh tokens.
- Protected API endpoints.
- Custom user model.

### Business Management

- Create and manage businesses.
- Business membership system.
- Business roles:
  - Owner
  - Manager
  - Staff
- Active and inactive memberships.
- Business-level data isolation.

### Products and Categories

- Create product categories.
- Create, update, list, and retrieve products.
- Product SKU management.
- Product units:
  - Bottle
  - Litre
  - Crate
  - Piece
- Buying and selling prices.
- Current stock quantity.
- Reorder levels.
- Low-stock detection.
- Product ownership validation.

### Inventory

- Stock increases through completed purchases.
- Stock decreases through completed sales.
- Stock movement history.
- Purchase, sale, adjustment, and return movement types.
- Overselling prevention.
- Stock balance tracking.
- Business and product ownership checks.

### Purchases

- Create purchase records.
- Add multiple products to a purchase.
- Track suppliers.
- Calculate purchase totals.
- Complete purchases.
- Increase stock after purchase completion.
- Cancel draft purchases.
- Prevent invalid purchase transitions.

### Sales

- Create sales with multiple products.
- Invoice number tracking.
- Payment methods:
  - Cash
  - M-Pesa
  - Card
  - Credit
- Discount support.
- Stock availability checks.
- Automatic stock deduction.
- Buying and selling price snapshots.
- Revenue calculation.
- Cost calculation.
- Gross profit calculation.
- Sale completion and cancellation workflows.

### Suppliers

- Create and manage suppliers.
- Supplier contact information.
- Supplier addresses and notes.
- Business-specific supplier records.
- Duplicate supplier prevention.

### Deliveries

- Create delivery orders for completed sales.
- Customer name and phone.
- Delivery address.
- Delivery fee.
- Assign delivery staff.
- Delivery status tracking:
  - Pending
  - Assigned
  - Out for delivery
  - Delivered
  - Cancelled
- Delivery transition validation.

### Reports and Dashboard

- Today's sales count.
- Today's revenue.
- Today's gross profit.
- Active product count.
- Low-stock product count.
- Total stock value.
- Pending deliveries.
- Sales by payment method.
- Top-selling products.
- Low-stock products.
- Recent sales.
- Recent purchases.

---

## Technology Stack

### Backend

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite for local development
- PostgreSQL planned for production
- Django CORS Headers

### Frontend

- React
- Vite
- Tailwind CSS v4
- React Router
- Axios
- Lucide React
- Recharts
- Responsive SaaS dashboard interface
- Light and dark theme support

### Development Tools

- Git
- GitHub
- Postman or Insomnia
- Docker
- Render or another cloud platform
- Bash automation scripts

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
│   ├── businesses/
│   ├── products/
│   ├── inventory/
│   ├── sales/
│   ├── suppliers/
│   ├── deliveries/
│   └── reports/
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
        │   └── AuthContext.jsx
        │
        ├── data/
        │   └── landingPage.js
        │
        ├── services/
        │   ├── api.js
        │   ├── auth.js
        │   └── dashboard.js
        │
        ├── pages/
        │   ├── auth/
        │   │   └── Login.jsx
        │   └── dashboard/
        │       └── Dashboard.jsx
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
        │   ├── layout/
        │   │   ├── AppLayout.jsx
        │   │   ├── Sidebar.jsx
        │   │   └── Topbar.jsx
        │   └── dashboard/
        │       ├── BusinessSnapshot.jsx
        │       ├── DashboardHeader.jsx
        │       ├── DashboardLoading.jsx
        │       ├── LowStock.jsx
        │       ├── MetricCard.jsx
        │       ├── PaymentMethods.jsx
        │       ├── RecentSales.jsx
        │       └── TopProducts.jsx
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
