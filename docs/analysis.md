# Analiză Teoretică - Algoritmi de Drum Minim

**Document:** analysis.md  
**Versiune:** 1.0  
**Data:** 3 martie 2026  
**Scop:** Analiza detaliată a algoritmilor de drum minim și modelarea matematică a problemei

---

## 1. Definiția Problemei

### 1.1 Formularea Problemei

**Problema Drumului Minim (Shortest Path Problem):**

Dat un graf ponderat $ G = (V, E) $ unde:
- $ V $ = mulțimea de noduri (intersecții)
- $ E $ = mulțimea de muchii (străzi)
- $ w: E \rightarrow \mathbb{R}^+ $ = funcție de pondere (distanță)

Găsiți **drumul cu pondere minimă** de la un nod sursă $ s \in V $ la un nod destinație $ t \in V $.

### 1.2 Definiții

- **Nod:** Entitate care reprezintă o intersecție în oraș
- **Muchie:** Legătura între două noduri (reprezentând o stradă)
- **Pondere:** Valoarea asociată unei muchii (distanță, timp, cost)
- **Drum:** Secvență de noduri conectate prin muchii consecutive
- **Lungimea drumului:** Suma ponderilor muchiilor din drum
- **Drum minim:** Drumul cu lungimea minimă între două noduri

### 1.3 Variante ale Problemei

| Variant | Descriere | Algoritm Util |
|---------|-----------|---------------|
| **Single Source** | O sursă, toate destinațiile | Dijkstra, Bellman-Ford |
| **Single Pair** | O sursă, o destinație specifică | A*, Dijkstra |
| **All Pairs** | Toate sursele, toate destinațiile | Floyd-Warshall |
| **Pondere Negativă** | Aceasta problemă permite și ponderi negative | Bellman-Ford |
| **Cicluri Negative** | Detecție cicluri cu pondere negativă | Bellman-Ford |

---

## 2. Modelarea Matematică a Orașului ca Graf Ponderat

### 2.1 Reprezentarea Formală

Unui oraș îi corespunde un graf $ G = (V, E, w) $:

$$
V = \{v_0, v_1, \ldots, v_{n-1}\}
$$

unde fiecare $ v_i $ reprezintă o intersecție.

$$
E = \{(u, v) : u, v \in V\}
$$

unde fiecare muchie $(u, v)$ reprezintă o stradă care conectează intersecțiile $u$ și $v$.

$$
w(u, v) \geq 0 \text{ pentru } (u, v) \in E
$$

funcția de pondere asociază fiecărei muchii o valoare pozitivă (distanță în km, timp în minute, etc.).

### 2.2 Reprezentări Computaționale

#### 2.2.1 Lista de Adiacență

```python
# Reprezentare internă
adjacency_list = {
    0: [(1, 450), (3, 950)],      # nodul 0 conectat cu 1 (450) și 3 (950)
    1: [(0, 450), (2, 320)],      # nodul 1 conectat cu 0 și 2
    2: [(1, 320), (3, 680)],      # ... și așa mai departe
    3: [(0, 950), (2, 680), (4, 250)],
    4: [(3, 250)]
}
```

**Avantaje:** Eficientă pentru grafuri rare; utilizare memorie $O(|V| + |E|)$

**Dezavantaje:** Acces lent pentru verificarea unei muchii specifice

#### 2.2.2 Matrice de Adiacență

```python
# Reprezentare matriceală
import numpy as np
adjacency_matrix = np.array([
    [0,   450, inf, 950, inf],
    [450, 0,   320, inf, inf],
    [inf, 320, 0,   680, inf],
    [950, inf, 680, 0,   250],
    [inf, inf, inf, 250, 0  ]
])
```

**Avantaje:** Acces rapid $ O(1) $ la orice muchie; operații matriceale ușoare

**Dezavantaje:** Utilizare memorie $ O(|V|^2) $; ineficientă pentru grafuri rare

### 2.3 Proprietăți ale Grafului Urban

1. **Conexitate:** Graful trebuie să fie conex (toate nodurile accesibile)
2. **Ponderi pozitive:** În contexte reale (distanță, timp), ponderi $w(e) \geq 0$
3. **Simetrie (parțială):** Unele straturi sunt bidirecționale, altele unidirecționale
4. **Densitate:** Grafurile urbane sunt relativ rare: $|E| \ll |V|^2$
5. **Euclidian:** Ponderea unei muchii $(u, v)$ spuneapproximativ proporțional cu distanța euclidiană

---

## 3. Prezentarea Algoritmilor

### 3.1 Algoritmul Dijkstra

#### 3.1.1 Istorie și Context

- **Inventator:** Edsger W. Dijkstra (1956)
- **Articol original:** "A Note on Two Problems in Connexion with Graphs"
- **Motivare:** Găsirea celui mai scurt drum în rețele de comunicații

#### 3.1.2 Descrierea Algoritmului

**Principiu:** Greedy - explorează nodurile cel mai apropiat de sursă, expandând progresiv raza.

**Pseudocod:**

```
DIJKSTRA(G, s):
    distanta[s] ← 0
    pentru fiecare v ∈ V \ {s}:
        distanta[v] ← ∞
    
    Q ← mulțimea vidă (priority queue)
    pentru fiecare v ∈ V:
        Q.adăugare(v, distanta[v])
    
    cât timp Q nu este vidă:
        u ← Q.extrage_minim()
        pentru fiecare muchie (u, v):
            dacă distanta[u] + w(u, v) < distanta[v]:
                distanta[v] ← distanta[u] + w(u, v)
                piesa[v] ← u              # Pentru reconstrucția drumului
                Q.actualizeaza(v, distanta[v])
    
    returnează distanta, piesa
```

#### 3.1.3 Exemplu de Execuție

**Intrare:** Graf cu noduri {0, 1, 2, 3, 4}, sursă = 0

| Pas | Nod Selectat | Distanțe | Noduri Vizitate |
|-----|--------------|----------|-----------------|
| 0 | - | [0, ∞, ∞, ∞, ∞] | {} |
| 1 | 0 | [0, 450, ∞, 950, ∞] | {0} |
| 2 | 1 | [0, 450, 770, 950, ∞] | {0, 1} |
| 3 | 2 | [0, 450, 770, 950, 1200] | {0, 1, 2} |
| 4 | 4 | [0, 450, 770, 950, 1200] | {0, 1, 2, 4} |
| 5 | 3 | [0, 450, 770, 950, 1200] | {0, 1, 2, 3, 4} |

#### 3.1.4 Avantaje și Dezavantaje

| Avantaj | Dezavantaj |
|---------|-----------|
| Optimal pentru ponderi pozitive | Nu funcționează cu ponderi negative |
| Eficient cu priority queue | Complexitate logaritmică cu PQ |
| Intuițiv și ușor de implementat | Caută toate destinațiile (nu e anumit pair) |
| Bine testat și stabil | Memoria pentru reconstrucție drum |

#### 3.1.5 Cazuri de Utilizare

- **Google Maps:** Pentru calcularea rutelor car/public transport cu ponderi pozitive
- **Rețele de calculatoare:** OSPF (Open Shortest Path First) protocol
- **Jocuri video:** Pathfinding cu costuri uniforme

### 3.2 Algoritmul Bellman-Ford

#### 3.2.1 Istorie și Context

- **Inventatori:** Richard Bellman (1958) și Lester Ford Jr. (1956)
- **Motivare:** Handle grafuri cu ponderi negative și detecție cicluri negative

#### 3.2.2 Descrierea Algoritmului

**Principiu:** Relaxare iterativă - repeți actualizarea distanțelor până la convergență.

**Pseudocod:**

```
BELLMAN_FORD(G, s):
    distanta[s] ← 0
    pentru fiecare v ∈ V \ {s}:
        distanta[v] ← ∞
    
    pentru i ← 1 la |V| - 1:
        pentru fiecare muchie (u, v) cu pondere w(u, v):
            dacă distanta[u] + w(u, v) < distanta[v]:
                distanta[v] ← distanta[u] + w(u, v)
                piesa[v] ← u
    
    # Detectare cicluri negative
    pentru fiecare muchie (u, v) cu pondere w(u, v):
        dacă distanta[u] + w(u, v) < distanta[v]:
            returnează "Ciclu negativ detectat"
    
    returnează distanta, piesa
```

#### 3.2.3 Exemplu de Execuție (cu ponderi negative)

**Graf special cu ponderi negative:**

Noduri: {0, 1, 2, 3}  
Muchii: (0→1: 4), (0→2: 2), (1→2: -3), (2→3: 2), (3→1: 1)

| Iterația | Distanțe |
|----------|----------|
| Inițial | [0, ∞, ∞, ∞] |
| După 1 | [0, 4, 2, 4] |
| După 2 | [0, 1, 2, 4] |
| După 3 | [0, 1, 2, 4] |

#### 3.2.4 Detectare Ciclu Negativ

Dacă după $ |V| - 1 $ iterații mai avem actualizări, înseamnă că există un ciclu negativ accesibil din sursă.

#### 3.2.5 Avantaje și Dezavantaje

| Avantaj | Dezavantaj |
|---------|-----------|
| Funcționează cu ponderi negative | Mult mai lent decât Dijkstra |
| Detecție cicluri negative | Complexitate $ O(VE) $ comparativ cu Dijkstra $ O((V+E)\log V) $ |
| Robust și stabil | Nu e potrivit pentru grafuri dense |
| Ușor de implementat | Găsește toate destinațiile |

#### 3.2.6 Cazuri de Utilizare

- **Găsire arbitraj:** Detectare oportunități de profit în schimburi valutare
- **Protocoale de rutare:** RIP (Routing Information Protocol)
- **Analiza costului:** Probleme cu costuri negative (subvenții, discounturi)

### 3.3 Algoritmul A* (A-Star)

#### 3.3.1 Istorie și Context

- **Inventatori:** Peter Hart, Nils Nilsson, Bertram Raphael (1968)
- **Motivare:** Dijkstra e ineficient pentru o singură pereche sursă-destinație (caut omnidirecțional)
- **Inovație:** Introducerea unei funcții heuristic pentru ghidarea căutării

#### 3.3.2 Descrierea Algoritmului

**Principiu:** Greedy cu ghidaj heuristic - prioritizează nodurile care par mai apropiate de destinație.

**Funcția de Evaluare:**

$$
f(n) = g(n) + h(n)
$$

unde:
- $g(n)$ = distanța efectivă de la sursă la nod $n$
- $h(n)$ = heuristica (estimare distanță de la $n$ la destinație)
- $f(n)$ = estimare distanță totală pe ruta prin $n$

**Pseudocod:**

```
A_STAR(G, s, t, h):
    deschis ← {s}                         # Noduri de explorat
    inchis ← {}                           # Noduri deja explorate
    g[s] ← 0                              # Cost real de la sursă
    f[s] ← h(s, t)                        # Estimare totală
    
    cât timp deschis nu este vidă:
        u ← extrage_minim(deschis, f)     # Nod cu cel mai mic f
        
        dacă u == t:
            returnează reconstruieste_drum(u)
        
        inchis ← inchis ∪ {u}
        pentru fiecare vecin v al lui u:
            dacă v ∈ inchis:
                continua
            
            g_nou ← g[u] + w(u, v)
            
            dacă v ∉ deschis:
                deschis ← deschis ∪ {v}
            dacă dacă g_nou < g[v]:
                g[v] ← g_nou
                f[v] ← g[v] + h(v, t)
                piesa[v] ← u
    
    returnează "Nu s-a găsit drum"
```

#### 3.3.3 Heuristici Comune

**1. Distanța Euclidiană** (pentru probleme 2D)

$$
h(n, goal) = \sqrt{(x_n - x_{goal})^2 + (y_n - y_{goal})^2}
$$

```python
import math
def heuristica_euclidiana(node1, node2, coordonate):
    x1, y1 = coordonate[node1]
    x2, y2 = coordonate[node2]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

**2. Distanța Manhattan** (pentru grilă)

$$
h(n, goal) = |x_n - x_{goal}| + |y_n - y_{goal}|
$$

```python
def heuristica_manhattan(node1, node2, coordonate):
    x1, y1 = coordonate[node1]
    x2, y2 = coordonate[node2]
    return abs(x2 - x1) + abs(y2 - y1)
```

**3. Admisibilitate:** O heuristic este admisibilă dacă **NEVER** supraestimează distanța reală.

#### 3.3.4 Exemplu de Execuție

**Intrare:** Sursă = 0, Destinație = 4, cu heuristica euclidiană

| Pas | Nod Selectat | g(n) | h(n) | f(n) | Deschis |
|-----|--------------|------|------|------|---------|
| 1 | 0 | 0 | 1200 | 1200 | {1, 3} |
| 2 | 1 | 450 | 950 | 1400 | {3, 2} |
| 3 | 2 | 770 | 600 | 1370 | {3, 4} |
| 4 | 4 | 1200 | 0 | 1200 | {3} |

#### 3.3.5 Avantaje și Dezavantaje

| Avantaj | Dezavantaj |
|---------|-----------|
| Mult mai eficient pentru pereche sursă-destinație | Complexitate implementării cu heuristic corectă |
| Optimal dacă heuristic e admisibilă | Depinde de o bună heuristic |
| Ușor adaptat pentru cu restricții | Memorie mai mare decât Dijkstra |
| Folosit în practică (Google Maps, GPS) | Dacă heuristic e proastă, poate fi lent |

#### 3.3.6 Cazuri de Utilizare

- **GPS și Navigație:** Google Maps, Apple Maps, Waze
- **Jocuri Video:** Pathfinding NPC-uri cu heuristica Manhattan/Euclidiana
- **Robotică:** Planificarea mișcării roboților
- **Jocuri de Puzzle:** Rezolvare puzzle-uri cu BFS + heuristic

---

## 4. Analiza Complexității

### 4.1 Complexitatea Algoritmului Dijkstra

#### 4.1.1 Implementare cu Priority Queue (Binary Heap)

**Complexitate:**

$$
T(Dijkstra) = O((|V| + |E|) \log |V|)
$$

**Analiza:**
- **Inițializare:** $O(|V|)$ - inițializare distanțe și PQ
- **Extragere minim:** $|V|$ operații, fiecare $O(\log |V|)$ → $O(|V| \log |V|)$
- **Relaxare muchie:** $|E|$ operații în total, fiecare $O(\log |V|)$ → $O(|E| \log |V|)$
- **Total:** $O(|V| \log |V| + |E| \log |V|) = O((|V| + |E|) \log |V|)$

**Memoria:** $O(|V| + |E|)$ pentru liste de adiacență + $O(|V|)$ pentru PQ = $O(|V| + |E|)$

#### 4.1.2 Implementare cu Matrice (Dijkstra Naiv)

**Complexitate:**

$$
T(Dijkstra_{naive}) = O(|V|^2)
$$

**Analiza:**
- **Inițializare:** $O(|V|)$
- **Alegere nod minim:** $|V|$ iterații, fiecare selectare $O(|V|)$ → $O(|V|^2)$
- **Relaxare:** $O(|V|^2)$ în total
- **Total:** $O(|V|^2)$

**Memoria:** $O(|V|^2)$ pentru matrice de adiacență

### 4.2 Complexitatea Algoritmului Bellman-Ford

#### 4.2.1 Timp

**Complexitate:**

$$
T(Bellman-Ford) = O(|V| \times |E|)
$$

**Analiza:**
- **Iterații externe:** $|V| - 1$ iterații (în cel mai rău caz)
- **Fiecare iterație:** Verifică toate $|E|$ muchii
- **Operație pe muchie:** $O(1)$ (o comparație și posibil o atribuire)
- **Total:** $O(|V| \times |E|)$

#### 4.2.2 Memorie

**Memoria:** $O(|V| + |E|)$ pentru listă de adiacență + $O(|V|)$ pentru distanțe = $O(|V| + |E|)$

### 4.3 Complexitatea Algoritmului A*

#### 4.3.1 Timp (Cazul Mediu)

**Complexitate (în practică):** $O(|E|)$ cu o heuristic bună

**Analiza:**
- **Caz optim:** Dacă heuristic e perfectă, explorează doar nodurile pe drumul optim → $O(drumul \ optim)$
- **Caz mediu:** Cu heuristic bună, explorează mult mai puțin decât Dijkstra
- **Caz pesim:** Dacă heuristic e proastă, poate fi la fel de lent ca Dijkstra → $O((|V| + |E|) \log |V|)$

#### 4.3.2 Memorie

**Memoria:** $O(|V|)$ - pentru seturile "deschis" și "închis" - poate fi mai mare decât Dijkstra în practică

---

## 5. Comparație între Algoritmi

### 5.1 Tabel Comparativ

| Caracteristic | Dijkstra | Bellman-Ford | A* |
|---|---|---|---|
| **Complexitate Timp** | $O((V+E)\log V)$ | $O(V \times E)$ | $O(E)$ (practică) |
| **Complexitate Memorie** | $O(V+E)$ | $O(V+E)$ | $O(V)$ |
| **Ponderi Negative** | ❌ Nu | ✅ Da | ❌ Nu |
| **Cicluri Negative** | ❌ Nu | ✅ Detectează | ❌ Nu |
| **Optim** | ✅ Da | ✅ Da | ✅ Da (cu heuristic admisibilă) |
| **Simplitate Implementare** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Caz de Utilizare** | Single source all pairs | Ponderi negative | Single pair (Dijkstra optimizat) |
| **Viteza Practică** | Bună | Lentă | Excelentă |

### 5.2 Grafice de Performanță (Teoretice)

```
Timp de Execuție vs Numărul de Noduri

     Dijkstra ────────────
    /
   /
  /                  
 /  A* ─────────────
─────────────────────────────→ Noduri
Bellman-Ford ╱
           ╱
         ╱
        ╱
```

### 5.3 Alegerea Algoritmului

**Foloseste DIJKSTRA dacă:**
- Ponderi pozitive
- Trebuie toate distanțele de la o sursă
- Grafuri cu ponderi uniforme

**Foloseste BELLMAN-FORD dacă:**
- Pot exista ponderi negative
- Trebuie detecție cicluri negative
- Grafuri mici (pentru că e lent)
- Nedorești complexitate PQ

**Foloseste A* dacă:**
- Trebuie doar un drum sursă-destinație
- Poți defini o heuristic bună
- Vrei performanță maximă în practică
- Ponderi pozitive

---

## 6. Extensii și Variante Viitoare

### 6.1 Variante ale Problemei Drumului Minim

#### 6.1.1 Problem of All-Pairs Shortest Paths

Găsire drum minim între TOȚI perechile de noduri.

**Algoritm:** Floyd-Warshall

```
$T(Floyd-Warshall) = O(|V|^3)$
```

**Pseudocod:**

```
FLOYD_WARSHALL(G):
    dist ← copia(w)              # Inițializare cu ponderile muchiilor
    
    pentru k ← 0 la |V| - 1:
        pentru i ← 0 la |V| - 1:
            pentru j ← 0 la |V| - 1:
                dist[i][j] ← min(dist[i][j], dist[i][k] + dist[k][j])
    
    returnează dist
```

#### 6.1.2 K-Schimbări Cel Mai Scurt Drum

Găsire al k-lea cel mai scurt drum (nu doar cel mai scurt).

**Aplicații:**
- Găsire rute alternative în navigație
- Optimizare logistică cu redundanță

#### 6.1.3 Drum Minim ConstrainT

Găsire drum minim cu restricții (ex: maxim 3 stații, evitare anumite zone).

**Aplicații:**
- Rute care ocolesc zone periculoase
- Rute care trec prin anumite puncte

### 6.2 Variante cu Ponderi Dinamice

**Problem:** Ponderile muchiilor se schimbă în timp (trafic în timp real).

**Soluții:**
- **Upper bounds and Potentials:** Precomputare; update incrementali
- **Kinetic Shortest Paths:** Recalculare parțială
- **Stochastic Shortest Paths:** Modele probabilistice

### 6.3 Problema Rutării Vehiculelor (VRP)

**Generalizare:** Mai mulți vehicule trebuie să viziteze mai mulți clienti.

**Variante:**
- CVRP (Capacitated VRP)
- MDVRP (Multi-Depot VRP)
- VRPSD (VRP cu Stochastic Demand)

### 6.4 Rutare Multimodală

**Problem:** Combinație de moduri de transport (mașină + metrou + bicicletă).

**Aplicații:**
- Google Maps cu transport public
- Rute hibride urbane

### 6.5 Optimizare cu Învățare pe Mașină

**Introducere ML:**
- Rețele neuronale pentru predicție trafic
- Reinforcement Learning pentru ageți de rutare
- Combinare ML + algoritmi clasici

---

## 7. Concluzii

### 7.1 Rezumat

1. **Dijkstra:** Cel mai bun pentru grafuri cu ponderi pozitive; standard industrial
2. **Bellman-Ford:** Necesar pentru ponderi negative; mai lent dar mai robust
3. **A*:** Cea mai bună performanță practică pentru pereche sursă-destinație; folosit în GPS-uri

### 7.2 Facturi de Succes

- Calcularea corectă a complexității
- Alegerea potrivită a structurii de date (Heap, Matrice)
- Testare cuprinzătoare cu cazuri diverse
- Profilare și optimizare pentru date reale

### 7.3 Recomandări pentru Implementare

1. Start cu **Dijkstra** pe matrice (ușor, $O(V^2)$)
2. Optimizare la **Dijkstra cu PQ** (mai greu, $O((V+E)\log V)$ mai bun)
3. Implementare **Bellman-Ford** pentru robustețe
4. Finalizare cu **A*** cu heuristic euclidiană
5. Testare extensivă și benchmark

---

**Document Creat:** 3 martie 2026  
**Versiune:** 1.0 - Analysis & Planning Phase  
**Status:** ✅ Complet pentru Săptămâna 1

