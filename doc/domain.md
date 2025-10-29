
# Documento de Entidades y Atributos – Motor Cognitivo de Matching Inmobiliario

Este documento describe una propuesta de modelo de datos para el dominio recomendación de oportunidades de inversión inmobiliaria mediante grafos:

Las entidades Investor, Project y Sponsor son el núcleo del grafo Market y DealTerms proporcionan contexto económico PortfolioPosition y UserInteraction habilitan el aprendizaje personalizado Tag añade semántica interpretable

---

## 1 Investor

Representa al cliente que busca oportunidades de inversión

| Atributo       | Tipo       | Descripción |
|----------------|------------|-------------|
| id             | UUID       | Identificador único, anonimizado |
| segment        | Enum       | Tipo de inversor (retail, professional, institution) |
| risk_profile   | Enum       | Nivel de riesgo aceptado (conservative, moderate, aggressive) |
| horizon        | Enum       | Plazo de inversión esperado (short, medium, long) |
| ticket_min     | Decimal    | Inversión mínima que puede realizar |
| ticket_max     | Decimal    | Inversión máxima que puede realizar |
| jurisdictions_ok | Lista     | Mercados en los que el inversor puede invertir |
| esg_pref       | Decimal    | Preferencia en criterios ESG (0–1) |
| created_at     | Datetime   | Fecha de alta |

---

## 2 InvestorMandate

Recoge criterios y restricciones explícitas definidas por el inversor o por la institución que lo representa

| Atributo           | Tipo       | Descripción |
|--------------------|------------|-------------|
| id                 | UUID       | Identificador único |
| asset_types_allowed| Lista Enum | Tipos de activos permitidos |
| stages_allowed     | Lista Enum | Fases de inversión permitidas |
| geographies_allowed| Lista      | Regiones aprobadas |
| min_target_irr     | Decimal    | Rentabilidad interna mínima |
| max_ltv            | Decimal    | Apalancamiento máximo permitido |
| min_esg_score      | Decimal    | Puntuación ESG mínima |
| ticket_min         | Decimal    | Inversión mínima según mandato |
| ticket_max         | Decimal    | Inversión máxima según mandato |
| effective_from     | Date       | Inicio de vigencia |
| effective_to       | Date       | Fin de vigencia |

---

## 3 Project

Es la oportunidad de inversión concreta

| Atributo       | Tipo       | Descripción |
|----------------|------------|-------------|
| id             | UUID       | Identificador único |
| name           | String     | Nombre comercial o referencia |
| asset_type     | Enum       | Tipo de activo inmobiliario |
| stage          | Enum       | Fase del proyecto |
| city           | String     | Ciudad |
| country        | String     | País |
| lat, lon       | Decimal    | Coordenadas aproximadas |
| irr_est        | Decimal    | Rentabilidad interna estimada |
| yield_est      | Decimal    | Rentabilidad anual estimada |
| ltv            | Decimal    | Loan-to-Value estimado |
| risk_score     | Decimal    | Nivel de riesgo del proyecto |
| esg_score      | Decimal    | Puntuación ESG |
| min_ticket     | Decimal    | Inversión mínima requerida |
| horizon        | Enum       | Horizonte temporal esperado |
| currency       | Enum       | Moneda del proyecto |
| text_desc      | Text       | Descripción textual del proyecto |

---

## 4 Sponsor

Entidad (promotor, operador, ) responsable del proyecto

| Atributo           | Tipo       | Descripción |
|--------------------|------------|-------------|
| id                 | UUID       | Identificador único |
| name               | String     | Nombre de la entidad |
| reputation_score   | Decimal    | Indicador de reputación (0–1) |
| track_record_irr_avg | Decimal  | IRR medio histórico |
| deals_count        | Int        | Número de operaciones previas |
| focus_geos         | Lista      | Geografías de especialización |
| focus_asset_types  | Lista Enum | Tipos de activos de especialización |

---

## 5 DealTerms

Define la estructura económica del acuerdo

| Atributo             | Tipo     | Descripción |
|----------------------|----------|-------------|
| id                   | UUID     | Identificador único |
| structure            | Enum     | Tipo de estructura (direct, spv, fund, club_deal) |
| preferred_return_pct | Decimal  | Hurdle o rentabilidad mínima |
| management_fee_pct   | Decimal  | Comisión de gestión |
| performance_fee_pct  | Decimal  | Comisión sobre beneficios |
| lockup_months        | Int      | Meses de bloqueo |
| distribution_policy  | String   | Frecuencia de distribución (quarterly, annual, etc) |

---

## 6 Market

Contexto económico y sectorial del proyecto

| Atributo       | Tipo     | Descripción |
|----------------|----------|-------------|
| id             | String   | Identificador del mercado |
| city           | String   | Ciudad |
| country        | String   | País |
| vacancy_rate   | Decimal  | Tasa de vacancia |
| rent_growth    | Decimal  | Crecimiento de rentas |
| cap_rate_market| Decimal  | Cap rate medio |

---

## 7 PortfolioPosition

Representa inversiones pasadas o presentes de un inversor en proyectos

| Atributo        | Tipo     | Descripción |
|-----------------|----------|-------------|
| id              | UUID     | Identificador único |
| committed_amount| Decimal  | Capital comprometido |
| entry_date      | Date     | Fecha de entrada |
| exit_date       | Date     | Fecha de salida |
| status          | Enum     | Estado de la posición (active, exited) |
| currency        | Enum     | Moneda de inversión |

---

## 8 UserInteraction

Registra el comportamiento digital del inversor con los proyectos

| Atributo | Tipo     | Descripción |
|----------|----------|-------------|
| id       | UUID     | Identificador del evento |
| type     | Enum     | Tipo de interacción (view, click, save, inquire, invest) |
| ts       | Datetime | Marca temporal |
| weight   | Decimal  | Intensidad relativa de la interacción |

---

## 9 Tag

Categorías semánticas asociadas a proyectos o preferencias

| Atributo | Tipo   | Descripción |
|----------|--------|-------------|
| id       | UUID   | Identificador único |
| name     | String | Nombre del tag (ejemplo: "cerca de transporte") |
| type     | Enum   | Categoría del tag (location, strategy, esg, risk) |

---



