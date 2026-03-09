# Comparison Report

Total runs: 24

## Summary Metrics

| Name | Extractor | Chunker | PDFs | Docs | Chunks | Avg Chunk Size | Extract s | Chunk s | Index s | Query s | k | post-rerank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pypdf + recursive | pypdf | recursive | 3 | 52 | 175 | 840 | N/A | N/A | N/A | 2.88 |
| pypdf + token | pypdf | token | 3 | 52 | 61 | 2253 | N/A | N/A | N/A | 3.369 |
| pypdf + character | pypdf | character | 3 | 52 | 56 | 2397 | N/A | N/A | N/A | 3.593 |
| pypdf + nltk | pypdf | nltk | 3 | 52 | 56 | 2416 | N/A | N/A | N/A | 3.657 |
| pypdf + spacy | pypdf | spacy | 3 | 52 | 56 | 2425 | N/A | N/A | N/A | 3.721 |
| pypdf + semantic | pypdf | semantic | 3 | N/A | 0 | N/A | N/A | N/A | N/A | 2.848 |
| pymupdf + recursive | pymupdf | recursive | 3 | 52 | 174 | 834 | N/A | N/A | N/A | 2.668 |
| pymupdf + token | pymupdf | token | 3 | 52 | 60 | 2269 | N/A | N/A | N/A | 3.145 |
| pymupdf + character | pymupdf | character | 3 | 52 | 56 | 2362 | 10.344 | 0.001 | 3.387 | 4.037 |
| pymupdf + nltk | pymupdf | nltk | 3 | 52 | 55 | 2428 | 10.381 | 0.023 | 3.404 | 3.389 |
| pymupdf + spacy | pymupdf | spacy | 3 | 52 | 55 | 2436 | 10.33 | 1.952 | 3.404 | 3.335 |
| pymupdf + semantic | pymupdf | semantic | 3 | 52 | 131 | 1008 | 10.464 | 4.247 | 2.46 | 3.216 |
| pdfplumber + recursive | pdfplumber | recursive | 3 | 52 | 174 | 832 | N/A | N/A | N/A | 2.815 |
| pdfplumber + token | pdfplumber | token | 3 | 52 | 69 | 2028 | N/A | N/A | N/A | 3.172 |
| pdfplumber + character | pdfplumber | character | 3 | 52 | 56 | 2380 | 13.039 | 0.009 | 4.644 | 3.755 |
| pdfplumber + nltk | pdfplumber | nltk | 3 | 52 | 55 | 2447 | 12.988 | 0.009 | 4.501 | 3.797 |
| pdfplumber + spacy | pdfplumber | spacy | 3 | 52 | 56 | 2408 | 13.401 | 1.6 | 4.504 | 3.522 |
| pdfplumber + semantic | pdfplumber | semantic | 3 | 52 | 128 | 1040 | 13.168 | 5.556 | 3.43 | 3.631 |
| pdfminer + recursive | pdfminer | recursive | 3 | 52 | 199 | 725 | N/A | N/A | N/A | 2.337 |
| pdfminer + token | pdfminer | token | 3 | 52 | 64 | 2253 | N/A | N/A | N/A | 3.54 |
| pdfminer + character | pdfminer | character | 3 | 52 | 183 | 780 | 12.176 | 0.015 | 2.037 | 2.33 |
| pdfminer + nltk | pdfminer | nltk | 3 | 52 | 57 | 2464 | 12.374 | 0.007 | 3.88 | 3.442 |
| pdfminer + spacy | pdfminer | spacy | 3 | 52 | 58 | 2434 | 12.099 | 1.875 | 3.958 | 3.243 |
| pdfminer + semantic | pdfminer | semantic | 3 | 52 | 130 | 1068 | 12.476 | 5.291 | 3.21 | 3.705 |

## pypdf + recursive

- Extractor: `pypdf`
- Chunker: `recursive`
- Collection: `data/chroma/pdfs-pypdf-recursive`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 175
- Avg chunk size: 840
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 2.88

## **Question**
### ¿Cual es el paradigma que sigue el mecanismo de memoria Memento?

**Answer**

# Respuesta

Según el contexto proporcionado, el paradigma que sigue el mecanismo de memoria **Memento** es el **plan-and-act paradigm** (paradigma de planificación y acción).

En este paradigma, el planificador y el ejecutor operan en un **ciclo alternado** para avanzar iterativamente en la finalización de tareas. 

Memento integra tres módulos de memoria para facilitar esta coordinación:

1. **Case Memory** (Memoria de Casos): almacenamiento vectorizado de casos previos para planificación de alto nivel
2. **Subtask Memory** (Memoria de Subtareas): almacenamiento basado en texto de subtareas activas y sus resultados
3. **Tool Memory** (Memoria de Herramientas): registros basados en texto de interacciones de herramientas para cada subtarea

En la etapa de planificación, el Planner (Planificador) se instancia como un agente CBR (Case-Based Reasoning) impulsado por LLM, que recibe la instrucción de la tarea para coordinar efectivamente el proceso de razonamiento a largo plazo.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.2708 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2350 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1875 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1667 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/Memento.pdf (page: 7) | hybrid_score: 0.0778 | Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.0750 | BM25

## pypdf + token

- Extractor: `pypdf`
- Chunker: `token`
- Collection: `data/chroma/pdfs-pypdf-token`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 61
- Avg chunk size: 2253
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 3.369

**Answer**

# Respuesta

Según el documento, el paradigma que sigue el mecanismo de memoria Memento es el **paradigma de Razonamiento Basado en Casos (CBR - Case-Based Reasoning)**.

Específicamente, el documento establece que:

> "This CBR method mirrors human analogical learning, where previously encountered outcomes shape decision-making"

## Características principales del paradigma:

1. **Aprendizaje Analógico Humano**: El mecanismo refleja cómo los humanos aprenden de casos anteriores para tomar decisiones futuras.

2. **Principio Fundamental**: "Similar problems should have similar solutions" (Problemas similares deben tener soluciones similares).

3. **Recuperación por Similitud**: Utiliza similitud semántica para recuperar los K casos más cercanos del banco de casos, comparando el estado actual con estados pasados.

4. **Memoria Dinámica y Evolutiva**: El banco de casos crece continuamente, acumulando tanto éxitos como fracasos, permitiendo:
   - Análisis retrospectivo para evitar errores pasados
   - Trayectorias exitosas que guían la planificación futura

5. **Variantes**: Memento implementa tanto memoria **no-paramétrica** (recuperación por similitud) como **paramétrica** (con actualización de función Q para selección adaptativa de casos).

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2750 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.2150 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1595 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 15) | hybrid_score: 0.1300 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1111 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 0) | hybrid_score: 0.0875 | Vectorstore
- data/pdfs/Memento.pdf (page: 8) | hybrid_score: 0.0700 | Vectorstore

## pypdf + character

- Extractor: `pypdf`
- Chunker: `character`
- Collection: `data/chroma/pdfs-pypdf-character`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 56
- Avg chunk size: 2397
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 3.593

**Answer**

# Respuesta sobre el Patrón Memento

Basándome en el contexto proporcionado, **no hay información directa sobre el patrón de diseño "Memento"** en el documento presentado.

Sin embargo, puedo responder tu pregunta de forma general:

## El Paradigma del Patrón Memento

El patrón **Memento** sigue el paradigma de **Programación Orientada a Objetos (POO)** y se basa en los siguientes principios:

1. **Encapsulación**: Captura el estado interno de un objeto sin exponer su estructura interna.

2. **Separación de responsabilidades**: Divide la responsabilidad entre:
   - **Originador**: El objeto cuyo estado se desea guardar
   - **Memento**: Objeto que almacena el estado
   - **Cuidador**: Gestiona el historial de estados

3. **Reversibilidad**: Permite restaurar un objeto a un estado anterior, implementando funcionalidad de "deshacer/rehacer".

4. **Inmutabilidad**: El memento generalmente es inmutable para garantizar que el estado capturado no cambie.

---

**Nota**: Si tu pregunta está relacionada específicamente con el contenido del documento sobre Design Thinking y validación de hipótesis, por favor aclara la conexión para una respuesta más precisa.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.2762 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2350 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1875 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1667 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1153 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.0750 | BM25

## pypdf + nltk

- Extractor: `pypdf`
- Chunker: `nltk`
- Collection: `data/chroma/pdfs-pypdf-nltk`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 56
- Avg chunk size: 2416
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 3.657

**Answer**

# Respuesta

Según el documento, el paradigma que sigue el mecanismo de memoria de Memento es:

## **Memory-augmented Markov Decision Process (M-MDP)**

El documento especifica que Memento se formaliza como un **Proceso de Decisión de Markov aumentado con memoria (M-MDP)**, equipado con una **política neural de selección de casos** para guiar las decisiones de acción.

### Características principales del paradigm:

1. **Memoria episódica**: Las experiencias pasadas se almacenan en una memoria episódica, que puede ser:
   - **Diferenciable** (paramétrica)
   - **No paramétrica**

2. **Aprendizaje por refuerzo en línea**: La política se actualiza continuamente basándose en la retroalimentación del entorno a través de un **mecanismo de reescritura de memoria**.

3. **Mejora de política**: Se logra mediante una **lectura eficiente de memoria (recuperación)**, sin necesidad de actualizar los parámetros del LLM subyacente.

Este paradigma permite la **adaptación continua de bajo costo** sin requerir fine-tuning del modelo de lenguaje, lo que representa una alternativa eficiente a los enfoques tradicionales basados en gradientes.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2750 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.2150 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1304 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 1) | hybrid_score: 0.1167 | Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1033 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 0) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/Memento.pdf (page: 0) | hybrid_score: 0.0778 | Vectorstore

## pypdf + spacy

- Extractor: `pypdf`
- Chunker: `spacy`
- Collection: `data/chroma/pdfs-pypdf-spacy`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 56
- Avg chunk size: 2425
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 3.721

**Answer**

# Respuesta

Según el contexto proporcionado, el paradigma que sigue el mecanismo de memoria de **Memento** es:

## **Memory-augmented Markov Decision Process (M-MDP)**

### Características principales:

1. **Aprendizaje por refuerzo en línea basado en memoria** - Permite adaptación continua de bajo costo sin necesidad de ajustar los parámetros del LLM subyacente.

2. **Política de selección de casos neural** - Utiliza una política neural para guiar las decisiones de acción basándose en experiencias pasadas.

3. **Memoria episódica** - Las experiencias pasadas se almacenan en una memoria episódica que puede ser:
   - **Diferenciable** (paramétrica)
   - **No paramétrica**

4. **Mecanismo de reescritura de memoria** - La política se actualiza continuamente basándose en la retroalimentación del entorno.

5. **Mejora de política mediante lectura eficiente** - La mejora se logra a través de la recuperación eficiente de la memoria (retrieval).

### Ventaja clave:

Este paradigma permite el **aprendizaje continuo en tiempo real sin actualizaciones de gradientes**, lo que lo hace más eficiente que los enfoques tradicionales que requieren fine-tuning del modelo LLM.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2750 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.2150 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1304 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 1) | hybrid_score: 0.1167 | Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1033 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 0) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/Memento.pdf (page: 0) | hybrid_score: 0.0778 | Vectorstore

## pypdf + semantic

- Extractor: `pypdf`
- Chunker: `semantic`
- Collection: `data/chroma/pdfs-pypdf-semantic`

**Metrics**

- PDFs: 3
- Docs: N/A
- Chunks: 0
- Avg chunk size: N/A
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 2.848

**Answer**

# Patrón de Diseño Memento

Lamentablemente, no se proporcionó contexto en tu pregunta, por lo que no puedo darte una respuesta basada en documentación específica.

Sin embargo, puedo ofrecerte información general:

El patrón **Memento** sigue el paradigma de **Programación Orientada a Objetos (POO)** y se clasifica como un patrón de **comportamiento**.

## Características principales:

- **Encapsulación**: Captura el estado interno de un objeto sin violar su encapsulación
- **Restauración de estado**: Permite restaurar un objeto a un estado anterior
- **Separación de responsabilidades**: Divide la responsabilidad entre:
  - **Originador** (Originator): objeto cuyo estado se guarda
  - **Cuidador** (Caretaker): gestiona los mementos
  - **Memento**: almacena el estado

Si tienes un documento o contexto específico que desees que analice, por favor compártelo y podré darte una respuesta más precisa.

## pymupdf + recursive

- Extractor: `pymupdf`
- Chunker: `recursive`
- Collection: `data/chroma/pdfs-pymupdf-recursive`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 174
- Avg chunk size: 834
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 2.668

**Answer**

# Respuesta

Según el contexto proporcionado, el paradigma que sigue el mecanismo de memoria **Memento** es el **plan-and-act** (planificar y actuar).

Específicamente, el documento indica que:

> "Memento follows the plan-and-act paradigm (Erdogan et al., 2025), where the planner and executor operate in an alternating loop to iteratively advance task completion."

Este paradigma se caracteriza por:

1. **Alternancia entre dos etapas principales:**
   - **Case-Based Planning** (Planificación basada en casos)
   - **Tool-Based Execution** (Ejecución basada en herramientas)

2. **Operación en bucle iterativo:** El planificador y el ejecutor trabajan de manera alternada para avanzar progresivamente en la completación de tareas.

3. **Integración de tres módulos de memoria:**
   - Case Memory (almacenamiento vectorizado de casos previos)
   - Subtask Memory (almacenamiento de subtareas activas)
   - Tool Memory (registros de interacciones con herramientas)

Este enfoque permite que Memento aborde desafíos de razonamiento a largo plazo mediante la coordinación efectiva entre la planificación y la ejecución.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.2708 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2350 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1875 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1667 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/Memento.pdf (page: 7) | hybrid_score: 0.0778 | Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.0750 | BM25

## pymupdf + token

- Extractor: `pymupdf`
- Chunker: `token`
- Collection: `data/chroma/pdfs-pymupdf-token`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 60
- Avg chunk size: 2269
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 3.145

**Answer**

# Respuesta

Según el documento, el paradigma que sigue el mecanismo de memoria Memento es el de **Case-Based Reasoning (CBR)** o **Razonamiento Basado en Casos**.

Específicamente, el documento establece que:

> "This CBR method mirrors human analogical learning, where previously encountered outcomes shape decision-making"

## Características principales del paradigma CBR en Memento:

1. **Aprendizaje Analógico Humano**: El mecanismo refleja cómo los humanos aprenden de experiencias previas, donde los resultados anteriores moldean la toma de decisiones.

2. **Principio Fundamental**: Asume que "problemas similares deberían tener soluciones similares" (*similar problems should have similar solutions*).

3. **Recuperación por Similitud**: Utiliza similitud semántica para recuperar los K casos más cercanos del banco de casos, comparando el estado actual con estados pasados.

4. **Acumulación de Experiencias**: El banco de casos crece dinámicamente, acumulando tanto éxitos como fracasos, lo que permite:
   - Análisis retrospectivo para evitar errores pasados
   - Proporcionar trayectorias exitosas que guíen la planificación futura

Este enfoque permite que Memento realice **aprendizaje continuo sin necesidad de actualizar los parámetros del modelo de lenguaje**.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2750 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.2150 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1429 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 16) | hybrid_score: 0.1175 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 0) | hybrid_score: 0.1167 | Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1033 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 8) | hybrid_score: 0.0778 | Vectorstore

## pymupdf + character

- Extractor: `pymupdf`
- Chunker: `character`
- Collection: `data/chroma/pdfs-pymupdf-character`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 56
- Avg chunk size: 2362
- Extract time (s): 10.344
- Chunk time (s): 0.001
- Index time (s): 3.387
- Query time (s): 4.037

**Answer**

# Respuesta sobre el Patrón Memento

Basándome en el contexto proporcionado, que se enfoca en un proceso de **Design Thinking y validación de hipótesis**, debo aclarar que la pregunta sobre el patrón de diseño **Memento** no está directamente abordada en el documento.

Sin embargo, puedo responder sobre el paradigma del patrón Memento en general:

## El Patrón Memento sigue el paradigma de:

**Encapsulación del Estado y Separación de Responsabilidades**

El mecanismo de memoria Memento se basa en:

1. **Captura de Estado**: Guarda el estado interno de un objeto en un momento específico sin exponer su estructura interna.

2. **Separación de Responsabilidades**: Divide la responsabilidad entre:
   - **Originador**: El objeto cuyo estado se captura
   - **Memento**: El objeto que almacena el estado
   - **Cuidador**: El objeto que gestiona los mementos

3. **Paradigma Funcional/Imperativo**: Permite implementar funcionalidades como:
   - Deshacer/Rehacer (Undo/Redo)
   - Historial de cambios
   - Recuperación de estados anteriores

---

**Nota**: Si su pregunta se refiere a cómo este concepto se aplica al contexto del documento (validación y aprendizaje iterativo), el patrón Memento podría usarse para registrar hipótesis y aprendizajes en las "Tarjetas de Aprendizaje" mencionadas.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.2762 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2350 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1875 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1667 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1153 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.0750 | BM25

## pymupdf + nltk

- Extractor: `pymupdf`
- Chunker: `nltk`
- Collection: `data/chroma/pdfs-pymupdf-nltk`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 55
- Avg chunk size: 2428
- Extract time (s): 10.381
- Chunk time (s): 0.023
- Index time (s): 3.404
- Query time (s): 3.389

**Answer**

# Respuesta

Según el documento, el paradigma que sigue el mecanismo de memoria de Memento es el **paradigma de Razonamiento Basado en Casos (CBR - Case-Based Reasoning)**.

Específicamente, el documento establece que:

> "This design follows the mainstream CBR paradigm, which assumes that similar problems should have similar solutions"

## Características principales del paradigma CBR en Memento:

1. **Aprendizaje Analógico**: Espeja el aprendizaje analógico humano, donde los resultados previamente encontrados moldean la toma de decisiones.

2. **Recuperación por Similitud**: Recupera los K casos más cercanos del banco de casos calculando la similitud semántica entre el estado actual y los estados pasados.

3. **Memoria No Paramétrica**: Utiliza una memoria dinámica y en crecimiento que almacena trazas episódicas ricas (estado, acción, recompensa) en lugar de depender únicamente de la memoria paramétrica del LLM.

4. **Aprendizaje Continuo**: Permite que el agente aprenda de experiencias pasadas (tanto éxitos como fracasos) sin requerir actualización de parámetros del modelo.

Este enfoque permite que Memento mejore su desempeño sin necesidad de fine-tuning tradicional del LLM.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2400 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1917 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 1) | hybrid_score: 0.1750 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1429 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1033 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 16) | hybrid_score: 0.0875 | Vectorstore
- data/pdfs/Memento.pdf (page: 8) | hybrid_score: 0.0778 | Vectorstore

## pymupdf + spacy

- Extractor: `pymupdf`
- Chunker: `spacy`
- Collection: `data/chroma/pdfs-pymupdf-spacy`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 55
- Avg chunk size: 2436
- Extract time (s): 10.33
- Chunk time (s): 1.952
- Index time (s): 3.404
- Query time (s): 3.335

**Answer**

# Respuesta

Según el documento, el paradigma que sigue el mecanismo de memoria de Memento es el **paradigma de Razonamiento Basado en Casos (CBR - Case-Based Reasoning)**.

Específicamente, el documento establece que:

> "This CBR method mirrors human analogical learning, where previously encountered outcomes shape decision-making"

## Características principales del paradigma CBR en Memento:

1. **Aprendizaje Analógico Humano**: El mecanismo refleja cómo los humanos aprenden de experiencias previas, donde los resultados anteriormente encontrados moldean la toma de decisiones.

2. **Principio Fundamental**: Asume que "problemas similares deberían tener soluciones similares" (*similar problems should have similar solutions*).

3. **Recuperación por Similitud Semántica**: Utiliza el operador `ReadNP` que recupera los K casos más cercanos del banco de casos mediante similitud semántica entre estados actuales y pasados.

4. **Almacenamiento de Experiencias**: Acumula tanto éxitos como fracasos en un banco de casos que crece dinámicamente, permitiendo tanto evitar errores pasados como guiar futuras decisiones con trayectorias exitosas.

Este enfoque permite que Memento realice **aprendizaje continuo sin necesidad de actualizar los parámetros del modelo de lenguaje**.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2400 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1917 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 1) | hybrid_score: 0.1750 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1429 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1033 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 16) | hybrid_score: 0.0875 | Vectorstore
- data/pdfs/Memento.pdf (page: 8) | hybrid_score: 0.0778 | Vectorstore

## pymupdf + semantic

- Extractor: `pymupdf`
- Chunker: `semantic`
- Collection: `data/chroma/pdfs-pymupdf-semantic`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 131
- Avg chunk size: 1008
- Extract time (s): 10.464
- Chunk time (s): 4.247
- Index time (s): 2.46
- Query time (s): 3.216

**Answer**

# Respuesta

Basándome en el contexto proporcionado, **no se encuentra información sobre el patrón de diseño Memento o su paradigma de memoria**.

El documento presentado trata sobre un **proceso de Design Thinking** enfocado en:
- Descubrimiento del contexto y usuarios
- Validación de hipótesis
- Definición de desafíos
- Creación de perfiles de usuario

El contenido se centra en metodología de innovación y diseño centrado en el usuario, no en patrones de diseño de software como Memento.

## Para responder tu pregunta correctamente

Si deseas conocer sobre el patrón **Memento**, necesitaría contexto diferente que incluya información sobre:
- Patrones de diseño (Design Patterns)
- Arquitectura de software
- Mecanismos de captura y restauración de estado

¿Podrías proporcionar el contexto específico sobre patrones de diseño o el patrón Memento?

**Sources**

- data/pdfs/mural.pdf (page: 1) | hybrid_score: 1.0000 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.5000 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.2000 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1750 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1542 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1129 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.1111 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.0875 | Vectorstore

## pdfplumber + recursive

- Extractor: `pdfplumber`
- Chunker: `recursive`
- Collection: `data/chroma/pdfs-pdfplumber-recursive`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 174
- Avg chunk size: 832
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 2.815

**Answer**

# Respuesta

Basándome en el contexto proporcionado, **no hay información sobre el patrón de diseño "Memento" o su mecanismo de memoria** en el documento.

El documento presentado es una **guía de Design Thinking y metodología de innovación** que cubre:

- Validación de hipótesis
- Descubrimiento de usuarios
- Definición de desafíos
- Análisis de soluciones existentes
- Conceptualización de ideas

Sin embargo, **no contiene referencias al patrón Memento**, que es un concepto de programación/ingeniería de software.

## Sugerencia

Si deseas conocer sobre el paradigma del patrón Memento, necesitarías:
- Documentación sobre patrones de diseño (Design Patterns)
- Literatura sobre arquitectura de software
- Recursos sobre programación orientada a objetos

¿Podrías proporcionar contexto adicional o un documento que contenga información sobre el patrón Memento?

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.2708 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2350 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1667 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1625 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1000 | BM25
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.0778 | Vectorstore

## pdfplumber + token

- Extractor: `pdfplumber`
- Chunker: `token`
- Collection: `data/chroma/pdfs-pdfplumber-token`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 69
- Avg chunk size: 2028
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 3.172

**Answer**

# Respuesta

Según el documento, el mecanismo de memoria de Memento sigue el paradigma de **Case-Based Reasoning (CBR)** o **Razonamiento Basado en Casos**.

Específicamente, el documento establece que:

> "This CBR method mirrors human analogical learning, where previously encountered outcomes shape decision-making"

## Características principales del paradigma CBR en Memento:

1. **Aprendizaje Analógico**: Refleja cómo los humanos aprenden de casos anteriores para tomar decisiones futuras.

2. **Similitud de Problemas**: Sigue el principio fundamental de CBR que asume que "problemas similares deberían tener soluciones similares" (*similar problems should have similar solutions*).

3. **Recuperación por Similitud Semántica**: Utiliza la similitud semántica entre el estado actual y estados pasados para recuperar los K casos más relevantes del banco de casos.

4. **Acumulación de Experiencias**: El sistema acumula tanto éxitos como fracasos, permitiendo:
   - Análisis retrospectivo para evitar errores pasados
   - Trayectorias exitosas que guíen la planificación futura

Este enfoque permite que Memento realice **aprendizaje continuo** y mejore su desempeño de manera incremental a través de la experiencia acumulada.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2833 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.2400 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1595 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1300 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1175 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 8) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/Memento.pdf (page: 0) | hybrid_score: 0.0778 | Vectorstore

## pdfplumber + character

- Extractor: `pdfplumber`
- Chunker: `character`
- Collection: `data/chroma/pdfs-pdfplumber-character`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 56
- Avg chunk size: 2380
- Extract time (s): 13.039
- Chunk time (s): 0.009
- Index time (s): 4.644
- Query time (s): 3.755

**Answer**

# Respuesta

Basándome en el contexto proporcionado, **no hay información directa sobre el patrón de diseño "Memento"** en el documento presentado.

El documento se enfoca en un **proceso de Design Thinking y validación de hipótesis** para resolver problemas de movilidad urbana (específicamente relacionado con ciclismo y desplazamiento en bicicleta), pero no aborda patrones de diseño de software como Memento.

## Sin embargo, si la pregunta es general:

El patrón **Memento** sigue el paradigma de **Programación Orientada a Objetos (POO)** y se basa en:

- **Captura del estado**: Guardar el estado interno de un objeto en un momento específico
- **Restauración**: Permitir volver a un estado anterior sin violar la encapsulación
- **Separación de responsabilidades**: Usa tres componentes (Originator, Memento, Caretaker)

**Paradigma conceptual**: Preservación y recuperación de estados históricos de objetos.

---

¿Podrías aclarar si tu pregunta está relacionada con el contexto del documento de Design Thinking, o si es una pregunta independiente sobre patrones de diseño?

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.2762 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2350 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1875 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1667 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1153 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.0750 | BM25

## pdfplumber + nltk

- Extractor: `pdfplumber`
- Chunker: `nltk`
- Collection: `data/chroma/pdfs-pdfplumber-nltk`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 55
- Avg chunk size: 2447
- Extract time (s): 12.988
- Chunk time (s): 0.009
- Index time (s): 4.501
- Query time (s): 3.797

**Answer**

# Paradigma de Memoria en Memento

Según el contexto proporcionado, el mecanismo de memoria de Memento sigue el paradigma de **Razonamiento Basado en Casos (CBR - Case-Based Reasoning)**.

## Características principales:

1. **Aprendizaje Analógico**: Memento espeja el aprendizaje analógico humano, donde los resultados previamente encontrados moldean la toma de decisiones.

2. **Banco de Casos Episódico**: En lugar de depender únicamente de la memoria paramétrica del LLM (que es fija después del entrenamiento), Memento implementa razonamiento basado en casos en línea almacenando trazas episódicas ricas.

3. **Recuperación por Similitud Semántica**: El sistema recupera los K casos más cercanos del banco de casos calculando la similitud semántica entre el estado actual y los estados pasados, asumiendo que **problemas similares deben tener soluciones similares**.

4. **Crecimiento Continuo**: El banco de casos crece dinámicamente en línea, acumulando tanto éxitos como fracasos, permitiendo:
   - Análisis retrospectivo para evitar errores pasados
   - Trayectorias exitosas que guían prospectivamente la planificación futura

Este enfoque permite que Memento realice **aprendizaje continuo** sin necesidad de reentrenamiento del modelo base.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2833 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2400 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1917 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 1) | hybrid_score: 0.1750 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1429 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1300 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 8) | hybrid_score: 0.1175 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1111 | BM25+Vectorstore

## pdfplumber + spacy

- Extractor: `pdfplumber`
- Chunker: `spacy`
- Collection: `data/chroma/pdfs-pdfplumber-spacy`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 56
- Avg chunk size: 2408
- Extract time (s): 13.401
- Chunk time (s): 1.6
- Index time (s): 4.504
- Query time (s): 3.522

**Answer**

# Respuesta

Según el documento, el mecanismo de memoria de Memento sigue el paradigma de **Case-Based Reasoning (CBR)** o **Razonamiento Basado en Casos**.

Específicamente, el documento establece que:

> "This CBR method mirrors human analogical learning, where previously encountered outcomes shape decision-making"

## Características principales del paradigma:

1. **Aprendizaje Analógico Humano**: El método refleja cómo los humanos aprenden por analogía, donde los resultados previamente encontrados moldean la toma de decisiones.

2. **Principio Fundamental**: Asume que "problemas similares deberían tener soluciones similares" (*similar problems should have similar solutions*).

3. **Recuperación por Similitud Semántica**: En cada paso de planificación, el sistema recupera los K casos más cercanos del banco de casos calculando la similitud semántica entre el estado actual y los estados pasados.

4. **Almacenamiento de Experiencias**: El sistema acumula tanto éxitos como fracasos en una memoria episódica, permitiendo:
   - **Análisis retrospectivo**: Evitar errores pasados
   - **Guía prospectiva**: Orientar la planificación futura con trayectorias exitosas

Este enfoque permite que Memento realice **aprendizaje continuo sin necesidad de ajustar los parámetros del LLM** subyacente.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2833 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2400 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1917 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 1) | hybrid_score: 0.1750 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1429 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 0) | hybrid_score: 0.1250 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1033 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 8) | hybrid_score: 0.0778 | Vectorstore

## pdfplumber + semantic

- Extractor: `pdfplumber`
- Chunker: `semantic`
- Collection: `data/chroma/pdfs-pdfplumber-semantic`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 128
- Avg chunk size: 1040
- Extract time (s): 13.168
- Chunk time (s): 5.556
- Index time (s): 3.43
- Query time (s): 3.631

**Answer**

# Respuesta

Basándome en el contexto proporcionado, **no se encuentra información sobre el patrón de diseño Memento o su paradigma de memoria**.

El documento presentado trata sobre un **proceso de Design Thinking** enfocado en:
- Descubrimiento del contexto y usuarios
- Validación de hipótesis
- Definición de desafíos
- Creación de perfiles de usuario

El contenido se centra en metodología de innovación y diseño centrado en el usuario, no en patrones de diseño de software como el patrón Memento.

## Aclaración

Si deseas conocer sobre el **patrón Memento**, puedo informarte que:

El patrón Memento sigue el **paradigma de Programación Orientada a Objetos (POO)** y se basa en el principio de **capturar y externalizar el estado interno de un objeto** sin violar su encapsulación, permitiendo restaurarlo posteriormente.

Sin embargo, esta información **no proviene del contexto proporcionado**. ¿Podrías proporcionar documentación específica sobre patrones de diseño si deseas una respuesta basada en el contexto?

**Sources**

- data/pdfs/mural.pdf (page: 1) | hybrid_score: 1.0000 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.5000 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.2000 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1750 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1542 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1129 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.1078 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.0875 | Vectorstore

## pdfminer + recursive

- Extractor: `pdfminer`
- Chunker: `recursive`
- Collection: `data/chroma/pdfs-pdfminer-recursive`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 199
- Avg chunk size: 725
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 2.337

**Answer**

# Respuesta

Según el contexto proporcionado, el paradigma que sigue el mecanismo de memoria **Memento** es el **plan-and-act paradigm** (paradigma de planificación y acción).

En este paradigma:

- **El planificador y el ejecutor operan en un bucle alternado** para avanzar iterativamente en la finalización de tareas
- **Se integran tres módulos de memoria** para una coordinación efectiva:
  1. **Case Memory** (Memoria de Casos): almacenamiento vectorizado de casos previos para planificación de alto nivel
  2. **Subtask Memory** (Memoria de Subtareas): almacenamiento basado en texto de subtareas activas y sus resultados
  3. **Tool Memory** (Memoria de Herramientas): registros basados en texto de interacciones de herramientas para cada subtarea

Este enfoque permite abordar desafíos de razonamiento a largo plazo mediante la alternancia entre planificación y ejecución, manteniendo un registro estructurado de casos, subtareas y herramientas utilizadas.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.2708 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2350 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1528 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1500 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 7) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1167 | Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1000 | BM25
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.0875 | Vectorstore

## pdfminer + token

- Extractor: `pdfminer`
- Chunker: `token`
- Collection: `data/chroma/pdfs-pdfminer-token`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 64
- Avg chunk size: 2253
- Extract time (s): N/A
- Chunk time (s): N/A
- Index time (s): N/A
- Query time (s): 3.54

**Answer**

# Respuesta

Según el documento, el paradigma que sigue el mecanismo de memoria de Memento es el **Case-Based Reasoning (CBR)** o **Razonamiento Basado en Casos**.

## Características principales:

El documento especifica que:

1. **Aprendizaje Analógico**: El método CBR de Memento "espeja el aprendizaje analógico humano, donde los resultados previamente encontrados moldean la toma de decisiones"

2. **Principio Fundamental**: Sigue el supuesto de que "problemas similares deberían tener soluciones similares" (Wiratunga et al., 2024; Guo et al., 2025)

3. **Recuperación por Similitud**: En cada paso de planificación, el módulo de memoria recupera casos relevantes del banco de casos mediante el cálculo de similitud semántica entre el estado actual y estados pasados

4. **Banco de Casos Dinámico**: Mantiene un repositorio en crecimiento continuo de experiencias (tanto éxitos como fracasos) que permite:
   - Análisis retrospectivo para evitar errores pasados
   - Orientación prospectiva mediante trayectorias exitosas

En resumen, Memento utiliza un enfoque de **memoria episódica basada en casos** que permite al agente aprender de experiencias previas de manera similar a cómo lo hace el razonamiento humano.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2750 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.2150 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1595 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1278 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1208 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 8) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/mural.pdf (page: 6) | hybrid_score: 0.0700 | Vectorstore

## pdfminer + character

- Extractor: `pdfminer`
- Chunker: `character`
- Collection: `data/chroma/pdfs-pdfminer-character`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 183
- Avg chunk size: 780
- Extract time (s): 12.176
- Chunk time (s): 0.015
- Index time (s): 2.037
- Query time (s): 2.33

**Answer**

# Respuesta

Según el contexto proporcionado, el paradigma que sigue el mecanismo de memoria **Memento** es el **plan-and-act paradigm** (paradigma de planificación y acción).

En este paradigma:

- **El planificador y el ejecutor operan en un bucle alternado** para avanzar iterativamente en la finalización de tareas
- **Se integran tres módulos de memoria** para una coordinación efectiva:
  1. **Case Memory** (Memoria de Casos): almacenamiento vectorizado de casos previos para planificación de alto nivel
  2. **Subtask Memory** (Memoria de Subtareas): almacenamiento basado en texto de subtareas activas y sus resultados
  3. **Tool Memory** (Memoria de Herramientas): registros basados en texto de interacciones de herramientas para cada subtarea

Este enfoque permite abordar desafíos de razonamiento a largo plazo mediante la alternancia entre planificación y ejecución, manteniendo un registro estructurado de casos, subtareas y herramientas utilizadas.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.2762 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2350 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1528 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1500 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 7) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1167 | Vectorstore
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.1000 | BM25
- data/pdfs/mural.pdf (page: 5) | hybrid_score: 0.0875 | Vectorstore

## pdfminer + nltk

- Extractor: `pdfminer`
- Chunker: `nltk`
- Collection: `data/chroma/pdfs-pdfminer-nltk`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 57
- Avg chunk size: 2464
- Extract time (s): 12.374
- Chunk time (s): 0.007
- Index time (s): 3.88
- Query time (s): 3.442

**Answer**

# Respuesta

Según el documento, el mecanismo de memoria de Memento sigue el **paradigma de Razonamiento Basado en Casos (CBR - Case-Based Reasoning)**.

Específicamente, el documento establece:

> "This CBR method mirrors human analogical learning, where previously encountered outcomes shape decision-making"

## Características principales del paradigma CBR en Memento:

1. **Aprendizaje Analógico Humano**: El sistema espeja el aprendizaje analógico humano, donde los resultados previamente encontrados moldean la toma de decisiones.

2. **Principio Fundamental**: Asume que "problemas similares deberían tener soluciones similares" (*similar problems should have similar solutions*).

3. **Recuperación por Similitud**: En cada paso de planificación, el sistema recupera los K casos más cercanos del banco de casos calculando la similitud semántica entre el estado actual y los estados pasados.

4. **Almacenamiento de Experiencias**: El sistema acumula tanto éxitos como fracasos en una memoria episódica, permitiendo:
   - Análisis retrospectivo para evitar errores pasados
   - Trayectorias exitosas que guíen prospectivamente la planificación futura

Este enfoque permite que Memento realice **aprendizaje continuo sin necesidad de actualizar los parámetros del LLM** mediante gradientes.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2400 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1917 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 1) | hybrid_score: 0.1750 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1304 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1033 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 0) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/Memento.pdf (page: 8) | hybrid_score: 0.0778 | Vectorstore

## pdfminer + spacy

- Extractor: `pdfminer`
- Chunker: `spacy`
- Collection: `data/chroma/pdfs-pdfminer-spacy`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 58
- Avg chunk size: 2434
- Extract time (s): 12.099
- Chunk time (s): 1.875
- Index time (s): 3.958
- Query time (s): 3.243

**Answer**

# Respuesta

Según el documento, el mecanismo de memoria de Memento sigue el **paradigma de Razonamiento Basado en Casos (CBR - Case-Based Reasoning)**.

Específicamente, el documento establece:

> "This CBR method mirrors human analogical learning, where previously encountered outcomes shape decision-making"

## Características principales del paradigma:

1. **Aprendizaje Analógico Humano**: El sistema espeja el aprendizaje analógico humano, donde los resultados previamente encontrados moldean la toma de decisiones.

2. **Principio Fundamental**: Asume que "problemas similares deberían tener soluciones similares" (*similar problems should have similar solutions*).

3. **Recuperación por Similitud**: En cada paso de planificación, el sistema recupera los K casos más cercanos del banco de casos calculando la similitud semántica entre el estado actual y los estados pasados.

4. **Aprendizaje Continuo**: El banco de casos crece dinámicamente, acumulando tanto éxitos como fracasos, lo que permite:
   - Análisis retrospectivo para evitar errores pasados
   - Trayectorias exitosas que guían prospectivamente la planificación futura

Este enfoque permite que Memento realice aprendizaje continuo sin necesidad de actualizar los parámetros del LLM subyacente.

**Sources**

- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.8500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.6500 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.2400 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.1917 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 1) | hybrid_score: 0.1750 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1304 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 2) | hybrid_score: 0.1033 | BM25+Vectorstore
- data/pdfs/Memento.pdf (page: 0) | hybrid_score: 0.1000 | Vectorstore
- data/pdfs/Memento.pdf (page: 8) | hybrid_score: 0.0778 | Vectorstore

## pdfminer + semantic

- Extractor: `pdfminer`
- Chunker: `semantic`
- Collection: `data/chroma/pdfs-pdfminer-semantic`

**Metrics**

- PDFs: 3
- Docs: 52
- Chunks: 130
- Avg chunk size: 1068
- Extract time (s): 12.476
- Chunk time (s): 5.291
- Index time (s): 3.21
- Query time (s): 3.705

**Answer**

# Respuesta

Basándome en el contexto proporcionado, **no se encuentra información sobre el patrón de diseño Memento o su paradigma de memoria**.

El documento presentado trata sobre un **proceso de Design Thinking** enfocado en:
- Descubrimiento del contexto y usuarios
- Validación de hipótesis
- Definición de desafíos
- Creación de perfiles de usuario

**No contiene referencias a patrones de diseño de software como Memento.**

---

## Aclaración

Si buscas información sobre el **patrón Memento**, este es un patrón de diseño que sigue el **paradigma de Programación Orientada a Objetos (POO)** y se utiliza para:

- **Capturar y externalizar** el estado interno de un objeto sin violar la encapsulación
- **Restaurar** el objeto a un estado anterior
- Implementar funcionalidades como "deshacer/rehacer" (undo/redo)

¿Podrías proporcionar el contexto correcto o aclarar si tu pregunta se refiere a otro tema?

**Sources**

- data/pdfs/mural.pdf (page: 1) | hybrid_score: 1.0000 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.5000 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 7) | hybrid_score: 0.2933 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 8) | hybrid_score: 0.2000 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 0) | hybrid_score: 0.1750 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1542 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.1400 | Vectorstore
- data/pdfs/mural.pdf (page: 3) | hybrid_score: 0.1129 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 1) | hybrid_score: 0.1111 | BM25+Vectorstore
- data/pdfs/mural.pdf (page: 4) | hybrid_score: 0.0875 | Vectorstore
