# Reto UNIR – Recomendador Neo4j + GDS

## Descripción
Sistema de recomendación **Investor → Project** construido sobre Neo4j 5 y Graph Data Science (GDS), con scripts de Python para:

- Sembrar datos del dominio (inversores, proyectos, mercados, tags, etc.).
- Proyectar el grafo GDS, generar embeddings con **FastRP** y escribir similitudes con **KNN**.
- Obtener recomendaciones de proyectos para un inversor combinando similitud y un score por reglas de negocio (mandato/criterios).

---

## Arquitectura
- **Neo4j 5.20.0 Community** (con APOC y GDS).
- Contenedor **Python (CLI)** que ejecuta:
  - `src.seed_loader` – carga/actualiza el dataset de ejemplo.
  - `src.gds_train` – crea el grafo `gw`, calcula embeddings (FastRP) y similitudes (KNN) escribiendo `:SIMILAR_TO`.
  - `src.recommend` – devuelve el top-N de proyectos recomendados para un inversor.

### Relaciones principales del dominio
```
(Investor)-[:HAS_MANDATE]->(InvestorMandate)
(Investor)-[:PREFERS]->(Tag)
(Project)-[:HAS_TAG]->(Tag)
(Project)-[:SPONSORED_BY]->(Sponsor)
(Project)-[:LOCATED_IN]->(Market)
(Investor)-[:INTERACTED]->(UserInteraction)-[:ON]->(Project)
(Investor)-[:HELD]->(PortfolioPosition)-[:IN]->(Project)
```

### Relación escrita por GDS
```
(Investor)-[:SIMILAR_TO {score:<cosine>}]->(Project)   // vía KNN sobre embeddings FastRP
```

---

## Estructura
```
reto-unir-dataset/
├─ docker-compose.yml
├─ .env
├─ neo4j/
│  ├─ seed/       
│  └─ ...         
├─ data/          
└─ py/
   ├─ Dockerfile
   └─ src/
      ├─ config.py          
      ├─ seed_loader.py     
      ├─ gds_train.py       
      └─ recommend.py       
```

---

## Requisitos
- Docker + Docker Compose


## Configuración (docker-compose.yml)
Ajustado a Neo4j 5 y plugins:

```yaml
services:
  neo4j:
    image: neo4j:5.20.0-community
    container_name: gw-neo4j
    restart: unless-stopped
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: "${NEO4J_USER}/${NEO4J_PASSWORD}"
      NEO4J_server_memory_pagecache_size: "2G"
      NEO4J_server_memory_heap_initial__size: "2G"
      NEO4J_server_memory_heap_max__size: "2G"
      NEO4J_dbms_security_auth__enabled: "true"
      NEO4J_dbms_security_procedures_unrestricted: "apoc.*,gds.*"
      NEO4J_dbms_security_procedures_allowlist: "apoc.*,gds.*"
      NEO4J_apoc_export_file_enabled: "true"
      NEO4J_apoc_import_file_enabled: "true"
      NEO4J_apoc_import_file_use__neo4j__config: "true"
      NEO4J_PLUGINS: '["apoc","graph-data-science"]'
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs
      - ./data:/import
      - ./neo4j/seed:/seed
    healthcheck:
      test: ["CMD-SHELL", "cypher-shell -a bolt://localhost:7687 --encryption=false -u \"$NEO4J_USER\" -p \"$NEO4J_PASSWORD\" \"RETURN 1\" >/dev/null 2>&1"]
      interval: 5s
      timeout: 5s
      retries: 40
      start_period: 25s

  py:
    build:
      context: ./py
      dockerfile: Dockerfile
    image: ${PY_IMAGE}
    container_name: gw-py
    depends_on:
      neo4j:
        condition: service_healthy
    working_dir: /app
    environment:
      NEO4J_BOLT: ${NEO4J_BOLT}
      NEO4J_USER: ${NEO4J_USER}
      NEO4J_PASSWORD: ${NEO4J_PASSWORD}
    volumes:
      - ./py:/app
      - ./data:/data
      - ./neo4j/seed:/seed
    restart: unless-stopped

volumes:
  neo4j-data:
  neo4j-logs:
```

### Enviroment variables:  `.env`
```
# Neo4j
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j_pw_change_me
NEO4J_BOLT=bolt://neo4j:7687
NEO4J_HTTP=http://neo4j:7474

# Python container
PY_IMAGE=gwmatcher-py:latest


---

## Puesta en marcha
### Levantar servicios
```bash
docker compose up -d
```

### Sembrar datos
```bash
docker compose exec py python -m src.seed_loader
# salida esperada: "Seed completed."
```

### Entrenar GDS (proyectar, embeddings, similitud)
```bash
docker compose exec py python -m src.gds_train
# salida esperada:
# [GDS] FastRP: nodes=<N>, mutate_ms=<ms>
# [GDS] KNN: compared=<X>, written=<Y>
```

### Recomendar
```bash
docker compose exec py python -m src.recommend --inv inv-1 --n 5
# salida: JSON con proyectos recomendados
```

---

## ¿Qué hace cada script?
### `src.seed_loader`
- Crea constraints de unicidad (id) para labels principales.
- Inserta nodos de ejemplo: Investor, Project, Market, Sponsor, Tag.
- Crea relaciones base (`PREFERS`, `HAS_TAG`, `SPONSORED_BY`, `LOCATED_IN`, `INTERACTED`, `ON`, `HELD/IN`).

### `src.gds_train`
- Proyecta el grafo GDS `gw`.
- Ejecuta **FastRP** para generar embeddings.
- Ejecuta **KNN** para escribir `:SIMILAR_TO {score}`.
- Parámetros típicos: `topK=10`, `similarityCutoff=0.0`.

### `src.recommend`
- Obtiene candidatos Project para un inversor (`--inv`).
- Aplica filtros de mandato si existen.
- Calcula un `final_score = 0.7 * similarity + 0.3 * feat_score`.
- `feat_score` suma puntos si el proyecto cumple IRR, LTV, ESG, y ticket.



## Extender el dataset
- Añadir más inversores/mandatos.
- Crear más interacciones `INTERACTED` y `PREFERS`.
- Ajustar pesos de `feat_score` o añadir nuevas reglas.



```cypher
CREATE (i2:Investor {id:'inv-2', ticket_min:200000, ticket_max:800000, esg_pref:0.5});
CREATE (m2:InvestorMandate {id:'mand-2', asset_types_allowed:['Residential'], geographies_allowed:['ES'], stages_allowed:['Core','Development'], max_ltv:0.6, min_esg_score:0.5, ticket_min:250000, ticket_max:700000});
MERGE (i2)-[:HAS_MANDATE]->(m2);
MERGE (i2)-[:PREFERS]->(:Tag {id:'tag-core', name:'Core', type:'Strategy'});
```

## Ejemplos de uso
```bash
# Recomendar 3 proyectos para el inversor: inv-1
docker compose exec py python -m src.recommend --inv inv-1 --n 3
```

### Salida esperada
```json
[
  {
    "project_id": "proj-1",
    "name": "Madrid Resi Dev A",
    "country": "ES",
    "asset_type": "Residential",
    "stage": "Development",
    "irr_est": 0.18,
    "ltv": 0.55,
    "esg_score": 0.7,
    "min_ticket": 500000,
    "similarity": 0.99334,
    "feat_score": 1.0,
    "final_score": 0.995338
  }
]
```


## Reset rápido
```bash
# Parar y borrar volúmenes (pierdes datos)
docker compose down -v

# Arrancar limpio
docker compose up -d

# Sembrar y entrenar de nuevo
docker compose exec py python -m src.seed_loader
docker compose exec py python -m src.gds_train
```

