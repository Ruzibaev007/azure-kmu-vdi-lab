# Azure Trial Strategy

## Goal

The project models a realistic 50-user KMU environment while staying safe for an Azure Trial / Free account.

## Strategy

The full business environment is modeled logically in the CMDB:

- 50 employees
- 50 user accounts
- 50 endpoint assets
- 9 departments
- RBAC groups
- ITSM tickets
- Security policies
- Azure resources

Only a small number of physical cloud resources should be deployed.

## Trial-Safe Deployment

| Resource | Strategy |
|---|---|
| Users | Modeled in database |
| Assets | Modeled in CMDB |
| VMs | 1–3 max during testing |
| VM runtime | Deallocated when not used |
| Network | Small VNet + NSG |
| Monitoring | Low ingestion |
| Storage | Minimal |
| Premium services | Avoid unless necessary |

## Why Not 50 Physical VMs?

Deploying 50 real VMs would be expensive and unnecessary for a learning portfolio project.

Instead, this project demonstrates:

- architecture design
- identity model
- CMDB structure
- security baseline
- cost control
- API reporting
- operational thinking

## Azure Quota Findings

During testing, some regions returned quota limitations for the selected SKU.

This is documented as a real troubleshooting scenario and part of the learning process.

## Cost-Control Rules

- Deallocate VMs when idle
- Avoid AlwaysOn premium plans
- Keep monitoring ingestion low
- Prefer modeled infrastructure over physical resources
- Document all quota and deployment errors
