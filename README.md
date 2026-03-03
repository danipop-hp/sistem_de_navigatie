# Sistem de Navigație Urbană folosind Algoritmi de Drum Minim

> **Proiect universitar** — Durata: 8 săptămâni  
> **Domeniu:** Algoritmi și Structuri de Date, Inteligență Artificială  
> **Limbaj de implementare:** Python 3.11+

---

## Descrierea Proiectului

Acest proiect propune dezvoltarea unui **sistem de navigație urbană** care utilizează algoritmi clasici și euristici de drum minim pentru a calcula rute optime într-un graf ce modelează rețeaua stradală a unui oraș. Sistemul va permite utilizatorilor să introducă un punct de plecare și o destinație, urmând să primească ruta optimă în funcție de diferite criterii: distanță minimă, timp minim sau cost minim.

Proiectul integrează concepte fundamentale din teoria grafurilor, algoritmica avansată și vizualizarea datelor, oferind atât o perspectivă teoretică cât și una practică asupra problemei de navigație urbană.

---

## Scopul și Obiectivele

### Scop General

Implementarea și compararea algoritmilor de drum minim (Dijkstra, Bellman-Ford, A\*) aplicați pe un graf ponderat care modelează infrastructura urbană a unui oraș real sau sintetic, cu scopul de a oferi un sistem funcțional de navigație.

### Obiective Specifice

1. **Modelarea grafului urban** — Reprezentarea rețelei stradale ca graf ponderat direcționat/nedirecționat, cu noduri (intersecții) și muchii (segmente de stradă) ponderate prin distanță, timp sau cost.
2. **Implementarea algoritmilor** — Implementarea corectă și eficientă a algoritmilor Dijkstra, Bellman-Ford și A\* în Python.
3. **Analiza comparativă** — Măsurarea și compararea performanțelor algoritmilor în funcție de dimensiunea grafului și tipul datelor de intrare.
4. **Vizualizarea rezultatelor** — Afișarea grafică a rețelei urbane și a rutelor calculate folosind biblioteci de vizualizare.
5. **Interfața utilizator** — Crearea unei interfețe simple (CLI sau GUI minimalist) pentru interacțiunea cu sistemul.
6. **Testarea și validarea** — Acoperirea codului cu teste unitare și de integrare pentru garantarea corectitudinii.

---

## Arhitectura Propusă

```
sistem_de_navigatie/
│
├── src/                          # Codul sursă principal
│   ├── __init__.py
│   ├── graph/                    # Modulul de reprezentare a grafului
│   │   ├── __init__.py
│   │   ├── graph.py              # Clasa Graf (adiacențe, operații de bază)
│   │   ├── node.py               # Clasa Nod (intersecție urbană)
│   │   └── edge.py               # Clasa Muchie (segment stradal ponderat)
│   │
│   ├── algorithms/               # Modulul algoritmilor de drum minim
│   │   ├── __init__.py
│   │   ├── dijkstra.py           # Algoritmul Dijkstra
│   │   ├── bellman_ford.py       # Algoritmul Bellman-Ford
│   │   └── astar.py              # Algoritmul A* (A-Star)
│   │
│   ├── data/                     # Modulul de gestionare a datelor
│   │   ├── __init__.py
│   │   ├── loader.py             # Încărcarea datelor din fișiere externe
│   │   └── parser.py             # Parsarea formatelor (JSON, CSV, OSM)
│   │
│   ├── visualization/            # Modulul de vizualizare
│   │   ├── __init__.py
│   │   └── map_visualizer.py     # Afișarea grafului și a rutelor
│   │
│   └── utils/                    # Utilitare generale
│       ├── __init__.py
│       └── helpers.py            # Funcții auxiliare (măsurare timp, distanțe geografice)
│
├── tests/                        # Suite de teste
│   ├── __init__.py
│   ├── test_graph.py             # Teste pentru modulul graph
│   ├── test_dijkstra.py          # Teste pentru algoritmul Dijkstra
│   ├── test_bellman_ford.py      # Teste pentru algoritmul Bellman-Ford
│   └── test_astar.py             # Teste pentru algoritmul A*
│
├── data/                         # Date de intrare
│   ├── cities/                   # Seturi de date pentru orașe
│   └── maps/                     # Fișiere de hartă (format OSM/GeoJSON)
│
├── notebooks/                    # Jupyter Notebooks pentru analiză și demonstrații
│   └── explorare_date.py         # Explorare și vizualizare inițială a datelor
│
├── analysis.md                   # Analiză teoretică și matematică
├── requirements.txt              # Dependențe Python
└── README.md                     # Documentația principală (acest fișier)
```

### Diagrama Fluxului de Date

```
Date externe (OSM/CSV/JSON)
        │
        ▼
   [Parser/Loader]
        │
        ▼
   [Graf Ponderat]
        │
        ├──────────────────────────────┐
        ▼                              ▼
[Dijkstra / Bellman-Ford / A*]   [Vizualizare Rețea]
        │
        ▼
  [Rută Optimă]
        │
        ▼
[Vizualizare Rută + Statistici]
```

---

## Tehnologiile care vor fi Folosite

| Categorie               | Tehnologie / Bibliotecă     | Versiune  | Scop                                                       |
|-------------------------|-----------------------------|-----------|------------------------------------------------------------|
| Limbaj de programare    | **Python**                  | 3.11+     | Limbajul principal de implementare                         |
| Structuri de date graf  | **NetworkX**                | 3.x       | Reprezentarea și manipularea grafurilor                     |
| Date geografice         | **OSMnx**                   | 1.x       | Descărcarea și procesarea datelor din OpenStreetMap        |
| Vizualizare statică     | **Matplotlib**              | 3.x       | Grafice, hărți și diagrame de performanță                  |
| Vizualizare interactivă | **Folium**                  | 0.x       | Hărți interactive bazate pe Leaflet.js                     |
| Calcule numerice        | **NumPy**                   | 1.x       | Operații matematice și matriceale                          |
| Testare                 | **pytest**                  | 7.x       | Framework pentru teste unitare și de integrare             |
| Mediu de lucru          | **Jupyter Notebook**        | 6.x       | Explorare interactivă și demonstrații                      |
| Gestionare dependențe   | **pip / virtualenv**        | —         | Izolarea mediului de dezvoltare                            |
| Control versiuni        | **Git / GitHub**            | —         | Versionarea codului și colaborare                          |

---

## Roadmap Detaliat pe 8 Săptămâni

### Săptămâna 1 — Analiză și Planificare *(în curs)*
- [ ] Definirea cerințelor funcționale și non-funcționale
- [ ] Studiul teoriei grafurilor și algoritmilor de drum minim
- [ ] Crearea structurii de foldere și fișiere a proiectului
- [ ] Redactarea documentației inițiale (README.md, analysis.md)
- [ ] Configurarea mediului de dezvoltare și a repository-ului Git

### Săptămâna 2 — Proiectarea Structurilor de Date
- [ ] Proiectarea claselor `Node`, `Edge` și `Graph`
- [ ] Definirea interfeței (API intern) pentru modulul de graf
- [ ] Proiectarea schemei de date pentru inputul din fișiere externe
- [ ] Schița diagramelor UML (diagrama de clase)

### Săptămâna 3 — Implementarea Grafului Urban
- [ ] Implementarea clasei `Node` cu atribute geografice (latitudine, longitudine, id)
- [ ] Implementarea clasei `Edge` cu ponderi (distanță, timp, cost)
- [ ] Implementarea clasei `Graph` (lista de adiacență, operații CRUD)
- [ ] Implementarea `loader.py` și `parser.py` pentru date CSV/JSON
- [ ] Teste unitare pentru modulul `graph`

### Săptămâna 4 — Implementarea Algoritmului Dijkstra
- [ ] Implementarea algoritmului Dijkstra cu coadă de priorități (heap)
- [ ] Reconstrucția și returnarea drumului minim
- [ ] Gestionarea cazurilor limită (nod inaccesibil, graf deconectat)
- [ ] Teste unitare pentru `dijkstra.py`
- [ ] Benchmark inițial pe grafuri sintetice

### Săptămâna 5 — Implementarea Bellman-Ford și A\*
- [ ] Implementarea algoritmului Bellman-Ford cu detectarea ciclurilor negative
- [ ] Implementarea algoritmului A\* cu funcție euristică haversine
- [ ] Teste unitare pentru `bellman_ford.py` și `astar.py`
- [ ] Comparație preliminară a rezultatelor între cei 3 algoritmi

### Săptămâna 6 — Integrarea Datelor Reale și Vizualizare
- [ ] Integrarea cu OpenStreetMap via OSMnx pentru date reale
- [ ] Implementarea `map_visualizer.py` cu Matplotlib și Folium
- [ ] Vizualizarea grafului urban (noduri, muchii, ponderi)
- [ ] Vizualizarea rutelor calculate pe hartă interactivă
- [ ] Notebook Jupyter pentru demonstrații vizuale

### Săptămâna 7 — Analiză de Performanță și Optimizări
- [ ] Benchmark complet pe grafuri de dimensiuni variate (100, 1000, 10000 noduri)
- [ ] Profilarea codului și identificarea blocajelor de performanță
- [ ] Optimizări: structuri de date îmbunătățite, memoizare
- [ ] Grafice comparative (timp de execuție vs. dimensiunea grafului)
- [ ] Redactarea raportului de analiză comparativă

### Săptămâna 8 — Finalizare, Testare și Documentare
- [ ] Acoperire completă cu teste (unit tests + integration tests)
- [ ] Refactorizarea codului și respectarea convențiilor PEP 8
- [ ] Finalizarea documentației (README, docstrings, comentarii)
- [ ] Crearea prezentării finale (slides)
- [ ] Demo final al aplicației
- [ ] Predarea proiectului

---

## Instalare și Configurare *(va fi completat)*

```bash
# Clonarea repository-ului
git clone https://github.com/danipop-hp/sistem_de_navigatie.git
cd sistem_de_navigatie

# Crearea mediului virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# sau: venv\Scripts\activate  # Windows

# Instalarea dependențelor
pip install -r requirements.txt
```

---

## Utilizare *(va fi completat)*

Instrucțiunile de utilizare vor fi adăugate după implementarea sistemului (Săptămânile 3–6).

---

## Structura Testelor *(va fi completat)*

Testele vor fi scrise folosind `pytest` și vor acoperi:
- Operații de bază pe graf (adăugare/ștergere noduri și muchii)
- Corectitudinea drumurilor minime calculate
- Cazuri limită și scenarii de eroare

---

## Autor

**Dan-Ioan Pop**  
Facultatea de Matematică și Informatică  
Proiect pentru disciplina Algoritmi și Structuri de Date  

---

## Licență

Acest proiect este dezvoltat în scop academic și educațional.
