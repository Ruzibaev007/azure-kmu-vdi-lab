# ☁️ Azure KMU VDI Lab

> Production-like Azure Infrastructure, CMDB, ITSM and Zero-Trust Environment for a fictional 50-user company.

---

## 📋 Project Overview

This project simulates a realistic Small & Medium Business (KMU) IT environment running on Microsoft Azure.

The goal is to demonstrate practical skills in:

* ☁️ Azure Infrastructure
* 🖥️ Azure Virtual Desktop (AVD)
* 🔐 Zero Trust Security
* 🧩 CMDB Design
* 🎫 IT Service Management (ITSM)
* 👥 Identity & Access Management (RBAC)
* 📊 Monitoring & Reporting
* 💾 Backup & Recovery
* 🚀 FastAPI Development

All users, devices and business data are fictional.

---

# 🏢 Company Model

## Business Structure

```text
Management
│
├── IT
├── Human Resources
├── Accounting
├── Purchasing
├── Dispatching
├── Engineering
├── Warehouse
└── Production
```

### Company Size

| Resource           | Count |
| ------------------ | ----- |
| Employees          | 50    |
| User Accounts      | 50    |
| Assets             | 50    |
| Departments        | 9     |
| Tickets            | 10    |
| Security Policies  | 16    |
| Backup Policies    | 3     |
| Monitoring Sources | 5     |

---

# 🌐 Zero Trust Network Architecture

```text
                        Internet
                            │
                    Azure Firewall
                            │
                    Azure Virtual Network
                            │
 ┌────────────┬────────────┬────────────┬────────────┐
 │            │            │            │            │
IT         HR         Finance      Engineering   Production
VLAN10     VLAN12     VLAN13       VLAN20        VLAN40
 │            │            │            │            │
 │            └────────────┴────────────┘            │
 │                                                   │
 └────────────── Access only via policy ─────────────┘
```

### Network Segmentation

| Zone             | VLAN | Purpose           |
| ---------------- | ---- | ----------------- |
| IT-ZONE          | 10   | IT Administration |
| MGMT-ZONE        | 11   | Management        |
| HR-ZONE          | 12   | Human Resources   |
| FINANCE-ZONE     | 13   | Accounting        |
| PROCUREMENT-ZONE | 14   | Purchasing        |
| DISPATCH-ZONE    | 15   | Logistics         |
| ENG-ZONE         | 20   | Engineering       |
| WAREHOUSE-ZONE   | 30   | Warehouse         |
| PRODUCTION-ZONE  | 40   | Production        |

---

# 🧩 CMDB Architecture

Each employee owns:

```text
Employee
    │
    ├── User Account
    │
    └── Assigned Asset
             │
             ├── Hostname
             ├── IP Address
             ├── MAC Address
             ├── VLAN
             └── Security Policies
```

Example:

```text
Thomas Becker
│
├── User: t.becker
│
└── Asset: KMU-ASSET-003
      ├── Hostname: kmu-it-001
      ├── IP: 10.0.10.10
      ├── VLAN: 10
      ├── Zone: IT-ZONE
      ├── MFA Enabled
      └── BitLocker Enabled
```

---

# 🎫 IT Service Management (ITSM)

Supported ticket types:

* Incident
* Service Request
* Change Request
* Asset Request
* Security Event

Example workflow:

```text
User
 │
 ▼
Service Desk
 │
 ▼
Ticket Creation
 │
 ▼
Assignment
 │
 ▼
Resolution
 │
 ▼
Closure
```

---

# 🔐 Security Baseline

Implemented controls:

### Identity

* Multi-Factor Authentication (MFA)
* Password Policy
* Account Separation
* RBAC

### Endpoint Security

* BitLocker
* Microsoft Defender
* Windows Firewall
* USB Restrictions

### Remote Access

* Restricted RDP
* Admin-only access
* AVD Access Policies

### Monitoring

* Audit Logging
* Security Events
* Alerting Sources

---

# 💾 Backup & Recovery

```text
Production Data
       │
       ▼
Backup Policy
       │
       ▼
Recovery Point
       │
       ▼
Restore Testing
```

Configured:

* Daily Backup
* Weekly Backup
* Monthly Backup

---

# 📊 Monitoring

Monitoring Sources:

* Azure Monitor
* Log Analytics
* Security Events
* Infrastructure Health
* Backup Status

---

# 🚀 FastAPI API

### Core Endpoints

| Endpoint                  | Description         |
| ------------------------- | ------------------- |
| `/`                       | API Health          |
| `/dashboard`              | Executive Dashboard |
| `/employees`              | Employee Inventory  |
| `/assets`                 | Asset Inventory     |
| `/tickets`                | ITSM Tickets        |
| `/tickets/open`           | Open Tickets        |
| `/security/policies`      | Security Baseline   |
| `/security/events`        | Security Events     |
| `/reports/management`     | Management Report   |
| `/cmdb/relationships`     | CMDB Graph          |
| `/cmdb/asset/{asset_tag}` | Asset Details       |

---

# 📈 Dashboard Example

```json
{
  "employees": 50,
  "user_accounts": 50,
  "assets": 50,
  "tickets": 10,
  "security_policies": 16,
  "backup_policies": 3,
  "security_events": 3
}
```

---

# 🛠 Technology Stack

### Cloud

* Microsoft Azure
* Azure Virtual Desktop
* Azure Networking

### Backend

* Python
* FastAPI
* SQLite

### Infrastructure

* CMDB
* ITSM
* RBAC
* Zero Trust

### Security

* MFA
* BitLocker
* Microsoft Defender
* Audit Logging

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with:

✅ Azure Infrastructure Administration

✅ Azure Virtual Desktop

✅ CMDB Design

✅ IT Asset Management

✅ IT Service Management

✅ Security Baselines

✅ RBAC Concepts

✅ Zero Trust Architecture

✅ FastAPI Development

✅ Operational Reporting

✅ Troubleshooting & Documentation

---

# 👨‍💻 Author

https://github.com/Protector080322

IT Infrastructure • Cloud • Azure • Linux • Networking • Security

# **Deutschland **🇩🇪
