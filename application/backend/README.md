
# Recommender – Quarkus Skeleton (code-first)

Proyecto base Quarkus con endpoints y DTOs mínimos para el sistema de recomendación Investor → Project.
Incluye Swagger-UI y respuestas stub para que puedas iterar rápido.

# Roles

## 1. INVESTOR
End user who consumes recommendations.  

- **Can**: view/edit their profile, view projects (limited by mandate), receive recommendations, give feedback, add favorites, request information.  
- **Cannot**: view other investors’ data, change scoring weights, run GDS jobs, edit projects.  

---

## 2. SPONSOR
Provider of the deal/project (external partner or collaborator).  

- **Can**: view their own projects and relevant metrics (leads, requests), upload/update documents for their projects.  
- **Cannot**: view investors (only aggregated or anonymized leads), access other sponsors’ projects, change weights, or run jobs.  

---

## 3. DATA-ANALYST (Internal business & data team)
Responsible for curation, operational oversight, graph relevance and recommendations.  

- **Can**: explore the full catalog, view aggregated statistics, review/edit project metadata, approve/reject sponsor proposals, run scoring previews.  
- **Cannot**: change global weights or GDS pipelines in production (only in sandbox), access investor PII without consent.  
- **Can also**: run/review GDS jobs (projection, FastRP, KNN), adjust scoring weights in staging, validate explainability.  
- **Cannot**: access PII without justification; production changes are subject to **ADMIN** approval.  

---

## 4. ADMIN
Governance, security, and configuration.  

- **Can**: manage users/roles, approve global scoring weight changes, configure feature flags, manage limits and data retention.  
- **Cannot**: (by policy) export massive amounts of PII without full traceability.  