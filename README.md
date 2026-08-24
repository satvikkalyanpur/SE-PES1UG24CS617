# Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Problem Statement #12 — Healthcare & Telemedicine**
**Blood Bank Inventory & Emergency Donor Matcher**

PES University · Dept. of Computer Science & Engineering

| | |
|---|---|
| **Name** | *Satvik Kalyanpur* |
| **SRN** | *PES1UG24CS617* |
| **Section** | *K* |
| **Tool used** | draw.io (diagrams.net) |

---

## Problem Overview

Blood banks require a real-time stock management system that monitors blood component shelf lives
and triggers geo-targeted emergency notifications to matching eligible donors during critical
shortages. The system keeps a concurrency-safe inventory ledger, matches incoming emergency requests
against compatible stock, and — when stock falls short — broadcasts SMS alerts to eligible donors
within a 10 km radius of the requesting facility.

## Actors

- **Emergency Requester** — raises urgent blood unit requests, receives availability and reservation status
- **Blood Bank Manager** — registers, issues and discards units; responds to expiry alerts
- **Donor** — registers, is screened for eligibility, receives emergency SMS alerts
- **SMS Gateway** *(external)* — delivers broadcast alerts
- **Geolocation Service** *(external)* — resolves coordinates and computes the notification radius

## Use Cases

| UC ID | Use Case |
|---|---|
| UC-01 | Raise Emergency Blood Request |
| UC-02 | Check Inventory Availability — *included by UC-01* |
| UC-03 | Broadcast Donor Alert — *extends UC-01* |
| UC-04 | Manage Blood Inventory |
| UC-05 | Monitor Shelf Life |
| UC-06 | Register Donor |

`UC-01 «include» UC-02` — an emergency request always checks live inventory before responding.
`UC-03 «extend» UC-01` — the donor broadcast fires only when available stock is insufficient.

## Submission

[**`SE-PES1UG24CS617.pdf`**](SE-PES1UG24CS617.pdf) — contains all three deliverables:

1. **Requirements Table** — 5 functional requirements (FR-001 to FR-005) and 2 non-functional
   requirements (NFR-001, NFR-002), each with ID, type, description, priority, a measurable
   pass/fail acceptance criterion, and rationale.
2. **UML Use-Case Diagram** — all actors, system boundary, six use cases, with one «include» and
   one «extend» relationship.
3. **Use-Case Flow Specification** — UC-01 Raise Emergency Blood Request, with preconditions,
   postconditions, the main success scenario, and two alternate flows.
