# App Dependency Graph

This document describes the dependencies between Django apps in the Remedium HMS project.

## Dependency Diagram

```
core (no dependencies)
│
├── hospital
│   └── depends on: none
│
├── patients
│   └── depends on: hospital (Ward, Room FKs)
│
├── staff
│   └── depends on: none
│
├── appointments
│   └── depends on: patients (Patient FK), staff (Staff FK)
│
├── billing
│   └── depends on: patients (Patient FK)
│
├── medical_records
│   └── depends on: patients (Patient FK)
│
├── laboratory
│   └── depends on: patients (Patient FK)
│
├── pharmacy
│   └── depends on: patients (Patient FK), staff (Staff FK)
│
├── surgery
│   └── depends on: patients (Patient FK), staff (Staff FK)
│
├── care_monitoring
│   └── depends on: patients (Patient FK)
│
├── inventory
│   └── depends on: none
│
├── reporting
│   └── depends on: reads from all apps
│
├── notifications
│   └── depends on: none
│
└── integration
    └── depends on: patients (API)
```

## Dependency Order (for migrations)

1. `core` - Base utilities and context processors
2. `hospital` - Wards and Rooms (no dependencies)
3. `staff` - Staff and User management (no dependencies)
4. `patients` - Depends on `hospital` (Ward, Room FKs)
5. `appointments` - Depends on `patients`, `staff`
6. `billing` - Depends on `patients`
7. `medical_records` - Depends on `patients`
8. `laboratory` - Depends on `patients`
9. `pharmacy` - Depends on `patients`, `staff`
10. `surgery` - Depends on `patients`, `staff`
11. `care_monitoring` - Depends on `patients`
12. `inventory` - Independent
13. `notifications` - Independent
14. `reporting` - Reads from all apps
15. `integration` - Depends on `patients` (API)

## Cross-App Relationships

| Source App | Target App | Relationship |
|------------|------------|--------------|
| patients | hospital | Patient → Ward (FK) |
| patients | hospital | Patient → Room (FK) |
| appointments | patients | Appointment → Patient (FK) |
| appointments | staff | Appointment → Staff (doctor FK) |
| billing | patients | Invoice → Patient (FK) |
| medical_records | patients | PatientDocument → Patient (FK) |
| laboratory | patients | LabTest → Patient (FK) |
| pharmacy | patients | Prescription → Patient (FK) |
| pharmacy | staff | Prescription → Staff (prescribed_by FK) |
| surgery | patients | Surgery → Patient (FK) |
| surgery | staff | Surgery → Staff (surgeon FK) |
| staff | staff | Shift → Staff (FK) |
| billing | billing | Payment → Invoice (FK) |

## Consolidation Recommendations

Based on the dependency analysis, these apps could be consolidated to reduce complexity:

1. **Clinical Group**: `hospital` + `care_monitoring` + `surgery`
   - All related to clinical/patient care operations
   - Would eliminate cross-app FK dependencies

2. **Resource Management**: `inventory` + `pharmacy`
   - Both manage supplies and medications
   - Shared logic for stock tracking

3. **Keep Separate** (good boundaries):
   - `patients` - Core domain entity
   - `staff` - Core domain entity
   - `appointments` - Scheduling logic
   - `billing` - Financial operations
   - `laboratory` - Specialized test management
   - `medical_records` - Document management
   - `reporting` - Analytics/BI
   - `notifications` - Messaging
   - `integration` - External APIs

## Notes

- `reporting` app reads from all other apps but has no FK dependencies
- `integration` provides external API adapters
- `core` provides shared utilities, context processors, and base templates
- All apps use `simple_history` for audit trails on key models
