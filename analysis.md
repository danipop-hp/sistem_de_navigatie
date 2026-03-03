# Analiză Teoretică — Sistem de Navigație Urbană

> **Document:** Analiză și Fundamentare Teoretică  
> **Proiect:** Sistem de navigație urbană folosind algoritmi de drum minim  
> **Săptămâna:** 1 — Analiză și Planificare

---

## Cuprins

1. [Definirea Problemei](#1-definirea-problemei)
2. [Modelarea Matematică a Orașului ca Graf Ponderat](#2-modelarea-matematică-a-orașului-ca-graf-ponderat)
3. [Prezentarea Algoritmilor](#3-prezentarea-algoritmilor)
   - 3.1 [Dijkstra](#31-algoritmul-dijkstra)
   - 3.2 [Bellman-Ford](#32-algoritmul-bellman-ford)
   - 3.3 [A* (A-Star)](#33-algoritmul-a-a-star)
4. [Analiza Complexității](#4-analiza-complexității)
5. [Comparație între Algoritmi](#5-comparație-între-algoritmi)
6. [Posibile Extensii Viitoare](#6-posibile-extensii-viitoare)

---

## 1. Definirea Problemei

### 1.1 Context

Navigarea eficientă într-un mediu urban reprezintă una dintre problemele fundamentale ale informaticii aplicate, cu impact direct în sisteme de tip GPS, aplicații de transport public, logistică urbană și mobilitate autonomă. Problema constă în determinarea **drumului optim** între două puncte dintr-o rețea stradală complexă, în funcție de unul sau mai multe criterii de optimizare.

### 1.2 Enunțul Formal al Problemei

**Date:**
- Un graf ponderat `G = (V, E, w)`, unde:
  - `V` = mulțimea nodurilor (intersecțiile sau punctele de interes din oraș)
  - `E ⊆ V × V` = mulțimea muchiilor (segmentele de stradă)
  - `w : E → ℝ⁺` = funcția de ponderare (distanță în metri, timp în secunde sau cost în unități monetare)
- Un nod sursă `s ∈ V` (punctul de plecare)
- Un nod destinație `t ∈ V` (punctul de sosire)

**Cerință:**
- Să se determine drumul `P = (s = v₀, v₁, v₂, ..., vₖ = t)` astfel încât suma ponderilor muchiilor parcurse să fie **minimă**.

**Funcția obiectiv:**
```
minimize: Σ w(vᵢ, vᵢ₊₁)  pentru i = 0, 1, ..., k-1
```

### 1.3 Variante ale Problemei

| Variantă | Descriere |
|----------|-----------|
| **SSSP** (Single-Source Shortest Path) | Drum minim de la o sursă la toate celelalte noduri |
| **STSP** (Single-Target Shortest Path) | Drum minim de la toate nodurile la o destinație fixă |
| **SSSP cu o singură pereche** | Drum minim între o sursă `s` și o destinație `t` |
| **All-Pairs Shortest Path (APSP)** | Drumuri minime între toate perechile de noduri |

Proiectul se concentrează pe **SSSP cu o singură pereche**, cel mai relevant pentru aplicațiile de navigație.

### 1.4 Restricții și Ipoteze de Lucru

- Ponderile muchiilor sunt **nenegative** (ipoteza principală pentru Dijkstra)
- Graful poate fi **direcționat** (pentru străzi cu sens unic) sau **nedirecționat**
- Se permite **graful deconectat** — sistemul trebuie să semnaleze absența drumului
- Funcția de ponderare poate fi **multi-criteriu** (distanță + timp + trafic)

---

## 2. Modelarea Matematică a Orașului ca Graf Ponderat

### 2.1 Elementele Grafului Urban

#### Noduri (Intersecții)
Fiecare intersecție sau punct de interes (POI) din oraș este reprezentat ca un nod `v ∈ V` cu atributele:
- **id**: identificator unic
- **latitudine** și **longitudine**: coordonate geografice WGS84
- **tip**: intersecție, stație de autobuz, punct de interes, etc.
- **grad** (degree): numărul de muchii incidente (numărul de străzi care se întâlnesc)

#### Muchii (Segmente Stradale)
Fiecare segment de stradă este o muchie `e = (u, v) ∈ E` cu atributele:
- **ponderea principală** `w(e)`: distanța în metri (calculată cu formula Haversine)
- **timp de traversare**: `w_t(e) = w(e) / v_medie`, unde `v_medie` este viteza medie pe acel segment
- **sens**: direcționat (sens unic) sau bidirecțional
- **tip stradă**: arteră principală, stradă secundară, alee, autostradă urbană, etc.

### 2.2 Formula Haversine pentru Distanța Geografică

Distanța reală între două puncte geografice se calculează cu **formula Haversine**:

```
a = sin²(Δlat/2) + cos(lat₁) · cos(lat₂) · sin²(Δlon/2)
c = 2 · atan2(√a, √(1−a))
d = R · c
```

unde:
- `lat₁, lon₁` și `lat₂, lon₂` sunt coordonatele celor două puncte (în radiani)
- `R = 6371 km` este raza medie a Pământului
- `d` este distanța în kilometri

### 2.3 Reprezentarea în Memorie

#### Lista de Adiacență (Adjacency List)
Reprezentare preferată pentru grafuri **sparse** (rare), tipice rețelelor urbane reale:
```
G[u] = [(v₁, w₁), (v₂, w₂), ..., (vₖ, wₖ)]
```
- **Spațiu:** `O(V + E)`
- **Avantaj:** Eficient pentru parcurgerea vecinilor unui nod

#### Matricea de Adiacență
Reprezentare pentru grafuri **dense** sau pentru operații matriceale:
```
A[i][j] = w(i, j)  dacă (i, j) ∈ E
A[i][j] = ∞        dacă (i, j) ∉ E
A[i][i] = 0
```
- **Spațiu:** `O(V²)` — ineficient pentru grafuri sparse urbane

#### Concluzie
Pentru rețelele urbane reale (sparse), **lista de adiacență** este reprezentarea optimă.

### 2.4 Exemplu de Graf Urban Simplificat

```
        A (Piața Centrală)
       / \
    2km   3km
     /     \
    B       C
(Gară)  (Spital)
     \     /
    4km   1km
       \ /
        D (Aeroport)
```

Graful corespunzător (nedirecționat, ponderat):
```
V = {A, B, C, D}
E = {(A,B,2), (A,C,3), (B,D,4), (C,D,1)}
```

Drumul minim de la A la D:
- Varianta 1: `A → B → D`, cost = 2 + 4 = **6 km**
- Varianta 2: `A → C → D`, cost = 3 + 1 = **4 km** ✓ (optim)

---

## 3. Prezentarea Algoritmilor

### 3.1 Algoritmul Dijkstra

#### Descriere
Propus de **Edsger W. Dijkstra** în 1956, acest algoritm rezolvă problema **SSSP** pentru grafuri cu ponderi **nenegative**. Utilizează o strategie **greedy** bazată pe o coadă de priorități.

#### Principiul de Funcționare
1. Inițializare: `dist[s] = 0`, `dist[v] = ∞` pentru toți `v ≠ s`
2. Se inserează sursa `s` în coada de priorități cu prioritatea 0
3. La fiecare pas:
   - Se extrage nodul `u` cu distanța minimă din coadă
   - Pentru fiecare vecin `v` al lui `u`:
     - Dacă `dist[u] + w(u,v) < dist[v]`:
       - `dist[v] = dist[u] + w(u,v)` (**relaxare**)
       - Se actualizează coada de priorități

#### Pseudocod
```
Dijkstra(G, s):
  dist[s] ← 0
  dist[v] ← ∞  pentru toți v ≠ s
  prev[v] ← NONE  pentru toți v
  Q ← min-priority-queue cu toate nodurile

  WHILE Q nu este goală:
    u ← EXTRACT-MIN(Q)
    FOR fiecare vecin v al lui u:
      alt ← dist[u] + w(u, v)
      IF alt < dist[v]:
        dist[v] ← alt
        prev[v] ← u
        DECREASE-KEY(Q, v, alt)

  RETURN dist[], prev[]
```

#### Reconstrucția Drumului
```
ReconstructPath(prev, s, t):
  path ← []
  current ← t
  WHILE current ≠ s:
    path.prepend(current)
    current ← prev[current]
  path.prepend(s)
  RETURN path
```

#### Cerințe
- Ponderile trebuie să fie **strict nenegative** (`w(e) ≥ 0`)
- Nu funcționează corect cu muchii de pondere negativă

---

### 3.2 Algoritmul Bellman-Ford

#### Descriere
Propus de **Richard Bellman** (1958) și **Lester Ford Jr.** (1956), acest algoritm rezolvă problema **SSSP** pentru grafuri cu ponderi **arbitrare** (inclusiv negative), detectând totodată **ciclurile de cost negativ**.

#### Principiul de Funcționare
1. Inițializare: `dist[s] = 0`, `dist[v] = ∞` pentru toți `v ≠ s`
2. Se repetă **|V| - 1** iterații:
   - Pentru fiecare muchie `(u, v)` din `E`:
     - Dacă `dist[u] + w(u,v) < dist[v]`: **relaxare**
3. Verificarea ciclurilor negative:
   - Dacă după `|V| - 1` iterații mai există relaxări posibile → ciclu negativ detectat

#### Pseudocod
```
BellmanFord(G, s):
  dist[s] ← 0
  dist[v] ← ∞  pentru toți v ≠ s
  prev[v] ← NONE  pentru toți v

  FOR i = 1 TO |V| - 1:
    FOR fiecare muchie (u, v, w) din E:
      IF dist[u] + w < dist[v]:
        dist[v] ← dist[u] + w
        prev[v] ← u

  // Detectarea ciclurilor negative
  FOR fiecare muchie (u, v, w) din E:
    IF dist[u] + w < dist[v]:
      RETURN "Ciclu negativ detectat!"

  RETURN dist[], prev[]
```

#### Avantaje față de Dijkstra
- Gestionează **ponderi negative**
- Detectează **cicluri de cost negativ**
- Mai simplu de implementat (fără coadă de priorități)

---

### 3.3 Algoritmul A* (A-Star)

#### Descriere
Algoritmul **A\*** (pronunțat "A-star"), propus de **Peter Hart, Nils Nilsson și Bertram Raphael** în 1968, este o extensie informată (euristică) a algoritmului Dijkstra. Utilizează o **funcție euristică** `h(v)` pentru a ghida căutarea spre destinație.

#### Principiul de Funcționare
A\* evaluează nodurile folosind funcția:

```
f(v) = g(v) + h(v)
```

unde:
- `g(v)` = costul real al drumului de la sursă `s` la nodul `v` (cunoscut)
- `h(v)` = estimarea euristică a costului de la `v` la destinația `t` (estimat)
- `f(v)` = estimarea costului total al drumului optim prin `v`

#### Proprietatea Admisibilității Euristicii
O euristică `h` este **admisibilă** dacă nu supraevaluează niciodată costul real:
```
h(v) ≤ h*(v)  pentru toți v ∈ V
```
unde `h*(v)` este costul real optim de la `v` la `t`.

#### Euristici pentru Navigație Geografică
- **Distanța Euclidiană:** `h(v) = √[(x_v − x_t)² + (y_v − y_t)²]`
- **Distanța Manhattan:** `h(v) = |x_v − x_t| + |y_v − y_t|`
- **Distanța Haversine:** Distanța geodezică pe suprafața Pământului (cea mai potrivită pentru navigație)

#### Pseudocod
```
AStar(G, s, t, h):
  openSet ← {s}
  gScore[s] ← 0
  fScore[s] ← h(s)
  prev[v] ← NONE  pentru toți v

  WHILE openSet nu este gol:
    u ← nodul din openSet cu fScore minim
    IF u = t:
      RETURN ReconstructPath(prev, s, t)

    openSet.remove(u)
    FOR fiecare vecin v al lui u:
      tentative_g ← gScore[u] + w(u, v)
      IF tentative_g < gScore[v]:
        prev[v] ← u
        gScore[v] ← tentative_g
        fScore[v] ← gScore[v] + h(v)
        IF v ∉ openSet:
          openSet.add(v)

  RETURN "Nu există drum de la s la t"
```

#### Optimalitate
A\* este **optimal și complet** dacă euristica este admisibilă și consistentă (monotonă):
```
h(u) ≤ w(u, v) + h(v)  pentru orice muchie (u, v)
```

---

## 4. Analiza Complexității

### 4.1 Complexitatea Algoritmului Dijkstra

| Implementare | Complexitate Timp | Complexitate Spațiu |
|---|---|---|
| Cu matrice de adiacență | `O(V²)` | `O(V²)` |
| Cu heap binar (binary heap) | `O((V + E) log V)` | `O(V + E)` |
| Cu heap Fibonacci | `O(E + V log V)` | `O(V + E)` |

**Notă:** Pentru grafuri sparse tipice rețelelor urbane (`E ≈ O(V)`), complexitatea cu heap binar devine `O(V log V)`.

### 4.2 Complexitatea Algoritmului Bellman-Ford

| Parametru | Valoare |
|---|---|
| Complexitate Timp | `O(V · E)` |
| Complexitate Spațiu | `O(V)` |

**Notă:** Semnificativ mai lent decât Dijkstra pentru grafuri mari, dar necesar când există ponderi negative.

### 4.3 Complexitatea Algoritmului A*

| Parametru | Valoare |
|---|---|
| Complexitate Timp (caz defavorabil) | `O(E)` = `O(b^d)` — exponențial în adâncimea drumului |
| Complexitate Timp (caz favorabil) | Sub-liniară față de Dijkstra cu euristică bună |
| Complexitate Spațiu | `O(V)` — stochează toate nodurile vizitate |

**Notă:** Performanța A\* depinde critic de calitatea euristicii. Cu o euristică perfectă, A\* vizitează doar nodurile de pe drumul optim.

### 4.4 Comparația Formală a Complexităților

```
Pentru un graf cu V noduri și E muchii (sparse: E ≈ k·V):

Dijkstra (heap binar):  O(E log V) = O(V log V)   ← cel mai rapid în practică
Bellman-Ford:           O(V · E)   = O(V²)         ← cel mai lent
A* (euristică bună):    O(E)       < O(V log V)     ← cel mai rapid cu euristică
```

---

## 5. Comparație între Algoritmi

### 5.1 Tabel Comparativ General

| Criteriu | Dijkstra | Bellman-Ford | A* |
|---|---|---|---|
| **Ponderi negative** | ✗ Nu | ✓ Da | ✗ Nu |
| **Detectare ciclu negativ** | ✗ Nu | ✓ Da | ✗ Nu |
| **Complexitate timp** | `O(E log V)` | `O(V·E)` | `O(E)` (cu h bună) |
| **Complexitate spațiu** | `O(V + E)` | `O(V)` | `O(V)` |
| **Utilizează euristică** | ✗ Nu | ✗ Nu | ✓ Da |
| **Drum unic (s→t)** | Suboptimal* | Suboptimal* | ✓ Optimizat |
| **Toate drumurile (s→*)** | ✓ Optim | ✓ Optim | ✗ Nu |
| **Ușurință implementare** | Medie | Ușor | Greu |
| **Potrivit pentru navigare GPS** | ✓ Da | ~ Posibil | ✓ Ideal |

*\*Dijkstra și Bellman-Ford calculează distanțele de la sursă la **toate** nodurile, deci „risipesc" calcule când ne interesează doar o destinație specifică.*

### 5.2 Scenarii de Utilizare Recomandate

| Scenariu | Algoritm Recomandat | Justificare |
|---|---|---|
| Navigare GPS în timp real | **A\*** | Viteza cea mai bună cu euristică geografică |
| Rețele cu sens unic și ponderi variate | **Dijkstra** | Simplu, eficient, ponderi nenegative |
| Grafuri cu costuri negative (ex: reduceri/bonificații) | **Bellman-Ford** | Singurul care gestionează ponderi negative |
| Detectarea buclelor de cost negativ | **Bellman-Ford** | Funcționalitate exclusivă |
| Generarea tuturor drumurilor minime dintr-o sursă | **Dijkstra** | Calculează SSSP complet |
| Grafuri extrem de mari (milioane de noduri) | **A\*** cu h bună | Minimizează nodurile vizitate |

### 5.3 Analiza Practică pentru Rețele Urbane

O rețea stradală urbană tipică are caracteristicile:
- **Sparse:** numărul de intersecții este mult mai mare decât numărul mediu de conexiuni per intersecție
- **Ponderi nenegative:** distanțele și timpii sunt pozitivi
- **Structură planar:** graful poate fi planificat pe o suprafață (stradă reală)
- **Date geografice:** coordonatele geografice permit definirea unor euristici admisibile

**Concluzie:** Pentru navigație GPS urbană, **A\*** este alegerea optimă. **Dijkstra** este o alternativă bună când nu există informații geografice sau când se doresc toate drumurile minime dintr-un nod. **Bellman-Ford** nu este recomandat pentru navigare în timp real, dar poate fi util pentru analize speciale.

---

## 6. Posibile Extensii Viitoare

### 6.1 Extensii Algoritmice

1. **Algoritmul Bidirectional Dijkstra**
   - Căutare simultană dinspre sursă și destinație
   - Reduce cu ~50% numărul de noduri vizitate față de Dijkstra clasic
   - Utilizat în sistemele GPS comerciale

2. **Algoritmul Contraction Hierarchies (CH)**
   - Preprocesare a grafului: eliminarea nodurilor de importanță scăzută
   - Interogări de drum minim de 1000× mai rapide față de Dijkstra
   - Utilizat de HERE Maps și Google Maps

3. **Hub Labeling**
   - Cel mai rapid algoritm pentru SSSP în grafuri rutiere cunoscut
   - Necesită spațiu suplimentar semnificativ pentru indexuri

4. **Algoritmul Floyd-Warshall**
   - Rezolvă **All-Pairs Shortest Path (APSP)**
   - Complexitate `O(V³)` — practic pentru grafuri mici
   - Util pentru analiza accesibilității unui întreg oraș

### 6.2 Extensii Funcționale

5. **Criterii de optimizare multiple**
   - Optimizare multi-obiectiv: minimizarea simultană a distanței, timpului și costului
   - Utilizarea frontului Pareto pentru soluții de compromis

6. **Date de trafic în timp real**
   - Integrarea cu API-uri de trafic (Google Traffic, HERE Traffic)
   - Actualizarea dinamică a ponderilor grafului
   - Re-calcularea rutei la schimbarea condițiilor

7. **Navigare pentru transport public**
   - Adăugarea stațiilor de autobuz/tramvai/metrou ca noduri speciale
   - Includerea timpilor de așteptare și a orarelor de transport
   - Algoritm time-dependent shortest path

8. **Suport pentru vehicule electrice**
   - Includerea stațiilor de încărcare ca constrângeri
   - Optimizarea rutei în funcție de autonomia bateriei
   - Probleme de tip „Vehicle Routing Problem (VRP)"

9. **Navigare pentru biciclete și pietoni**
   - Grafuri separate pentru diferite tipuri de utilizatori
   - Ponderi adaptate (pante, trotuare, piste cicloturistice)

10. **Sistem de predicție a traficului**
    - Modele de machine learning pentru predicția aglomerației
    - Actualizarea predictivă a ponderilor bazată pe ore de vârf

### 6.3 Extensii de Vizualizare

11. **Hartă 3D interactivă**
    - Vizualizarea altitudinii și reliefului urban
    - Integrare cu WebGL (via deck.gl sau Mapbox GL)

12. **Vizualizarea procesului algoritmic (animație)**
    - Animarea pas-cu-pas a algoritmilor pe hartă
    - Scop educațional și de demonstrație

### 6.4 Extensii de Infrastructură

13. **API REST**
    - Expunerea funcționalității de navigare ca serviciu web
    - Compatibilitate cu aplicații mobile și web

14. **Scalabilitate pe grafuri masive**
    - Paralelizarea algoritmilor pe multiple nuclee CPU
    - Procesare distribuită cu Apache Spark pentru grafuri de dimensiunea unui continent

---

*Document generat în cadrul Săptămânii 1 — Analiză și Planificare*  
*Implementarea va începe în Săptămâna 3*
