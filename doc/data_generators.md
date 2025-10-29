# Generadores de Datos Sintéticos para Neo4j

Este documento describe el diseño, la configuración y el flujo de trabajo de los generadores de datos sintéticos para poblar un grafo Neo4j. Se cubren los patrones de diseño empleados, el modelo probabilístico, la orquestación, la serialización a Cypher y las convenciones de extensión. Incluye diagramas UML en Mermaid.

---

## Objetivos

- Generar datos realistas y reproducibles para múltiples entidades de negocio.
- Controlar la distribución estadística de los datos mediante configuración YAML.
- Garantizar idempotencia en la carga a Neo4j usando `MERGE`.
- Facilitar la extensibilidad con un patrón Factory + Registry + Strategy y carga perezosa de módulos.

---

## Arquitectura y Patrones de Diseño

El sistema se basa en los siguientes componentes:

- **EntityGenerator (ABC)**: interfaz común con `generate(n) -> List[Dict]` que cada generador de entidad implementa.
- **GeneratorFactory (Factory + Registry)**: registro de generadores por nombre de entidad y creación dinámica de instancias.
- **Estrategias por entidad (`*_gen.py`)**: encapsulan reglas de generación, rangos, pesos y uso de Faker.
- **Serializadores (`cypher.py`)**: funciones `<entidad>_to_cypher(dict) -> str` que emiten `MERGE` idempotentes.
- **Orquestador (`runner.py`)**: lee YAMLs, carga perezosamente `.<entity>_gen`, invoca `generate`, y escribe `.cypher` o `.json`.
- **Cargador (`seed_loader.py`)**: recorre `/seed/**/*.cypher` en orden léxico y ejecuta los statements.

### Lazy load

- `synth/__init__.py` **no** importa los generadores.
- `runner.py` realiza `importlib.import_module(f".{entity}_gen", package="src.synth")` justo antes de `GeneratorFactory.create(...)`.
- Convención: el fichero se llama `src/synth/<entity>_gen.py` y registra `GeneratorFactory.register("<entity>", ...)`.

---

## Modelo Probabilístico y Reglas

- **Configuración YAML por entidad** (`/data/config/<entidad>.yaml`):
  - `count`: número de instancias a generar.
  - `defaults`: rangos numéricos y parámetros (p. ej., `irr_est_range`, `ltv_range`, `min_ticket_range`).
  - `enums`: valores categóricos con `weights` para muestreo ponderado.
  - Listas y subconjuntos: atributos como `focus_geos` o `asset_types_allowed` se generan con subconjuntos aleatorios controlados.
  - `random_seed`: garantiza reproducibilidad de `random`, `numpy.random` y Faker.

- **Selección categórica ponderada**: `random.choices(values, weights=...)`.
- **Rangos numéricos**: `uniform(lo, hi)` con posible `clamp`.
- **Heurísticas de dominio**: derivación de atributos (p. ej., `risk_score` como función de `IRR` y `LTV`).

---
