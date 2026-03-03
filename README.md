# Sistem de Navigație Urbană Folosind Algoritmi de Drum Minim

**Universitate:** [Completezi cu universitatea ta]  
**Facultate:** [Completezi cu facultatea ta]  
**Materie:** Algoritmi și Structuri de Date  
**Durata:** 8 săptămâni (martie - aprilie 2026)  
**Limbaj de Programare:** Python 3.8+

---

## 1. Descrierea Proiectului

Acest proiect implementează un sistem complet de navigație urbană care determină cea mai scurtă rută între două locații într-un oraș modelat ca graf ponderat. Sistemul compară performanța și caracteristicile a trei algoritmi clasici de găsire a drumului minim și oferă o interfață intuitivă pentru vizualizarea grafului și rutelor calculate.

**Contextul problemei:** Sistemele de navigație moderne (Google Maps, Waze, etc.) se bazează pe algoritmi sofisticați de găsire a drumului optim. Acest proiect explorează fundamentele acestor sisteme prin implementarea algoritmilor clasici și analiza comparativă a acestora.

---

## 2. Scopul și Obiectivele

### Scop general
Dezvoltarea unei aplicații de navigație urbană care demonstrează aplicabilitatea algoritmilor de drum minim în rezolvarea problemelor din lumea reală.

### Obiective specifice

1. **Modelarea problemei:** Reprezentarea unui oraș ca graf ponderat unde nodurile sunt intersecții și muchiile sunt străzi.

2. **Implementarea algoritmilor:** Codificarea a trei algoritmi diferiți pentru găsirea drumului minim:
   - Algoritmul Dijkstra
   - Algoritmul Bellman-Ford
   - Algoritmul A*

3. **Comparație și analiză:** Evaluarea performanței algoritmilor în termeni de:
   - Complexitate de timp și spațiu
   - Acuratețe
   - Scalabilitate
   - Cazuri de utilizare ideale

4. **Validare și testare:** Crearea unui set cuprinzător de teste unitare și de integrare.

5. **Documentație și prezentare:** Producerea de documente tehnice și materiale de prezentare profesionale.

---

## 3. Arhitectura Propusă

### 3.1 Componente principale

```
┌─────────────────────────────────────────────────────┐
│                   USER INTERFACE                     │
│            (Command Line / Visualization)            │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────┐
│              APPLICATION LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   Main.py    │  │  Route.py    │  │ Parser.py │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘ │
└─────────┼──────────────────┼──────────────────┼─────┘
          │                  │                  │
┌─────────┼──────────────────┼──────────────────┼─────┐
│   ALGORITHM LAYER          │                  │     │
│  ┌──────────────┬──────────┴────┬─────────────┴─┐  │
│  │  Dijkstra    │  Bellman-Ford │      A*       │  │
│  └──────┬───────┴────────┬──────┴───────┬───────┘  │
└─────────┼────────────────┼──────────────┼──────────┘
          │                │              │
┌─────────┼────────────────┼──────────────┼──────────┐
│     DATA STRUCTURE LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────┐ │
│  │   Graph.py   │  │   Node.py    │  │ Edge.py │ │
│  └──────────────┘  └──────────────┘  └─────────┘ │
└──────────────────────────────────────────────────┘
          │
┌─────────┴──────────────────────────────────────────┐
│            PERSISTENCE LAYER                        │
│         (Data Files / City Graphs)                 │
└────────────────────────────────────────────────────┘
```

### 3.2 Descrierea modulelor

| Modul | Fișier | Responsabilitate |
|-------|--------|-----------------|
| **Core Data Structures** | `src/models/` | Definirea claselor Node, Edge, Route |
| **Graph Management** | `src/graph.py` | Construirea și manipularea grafului |
| **Algoritmi** | `src/algorithms/` | Implementarea Dijkstra, Bellman-Ford, A* |
| **Utilities** | `src/utils/` | Parsare date, vizualizare grafuri |
| **Main Application** | `src/main.py` | Punct de intrare, interfață utilizator |
| **Testing** | `tests/` | Suite de teste unitare și de integrare |

---

## 4. Tehnologiile Care Vor Fi Folosite

### 4.1 Limbajul de programare
- **Python 3.8+** - Alegere motivată pentru claritate, simplitate și bibliotecile disponibile

### 4.2 Biblioteci principale

| Bibliotecă | Versiune | Utilizare |
|-----------|----------|-----------|
| **NetworkX** | 2.6.0+ | Manipulare și analiză grafuri |
| **Matplotlib** | 3.5.0+ | Vizualizare grafuri și rute |
| **NumPy** | 1.20.0+ | Operații numerice și calcule matriciale |

### 4.3 Instrumente de dezvoltare
- **Git** - Control de versiuni
- **unittest/pytest** - Framework-uri de testare
- **Python venv** - Mediu virtual izolat
- **VS Code / PyCharm** - Editor de cod

---

## 5. Roadmap Detaliat - 8 Săptămâni

### **SĂPTĂMÂNA 1: Analiză și Planificare** (19-23 martie)
- ✓ Definirea structurii proiectului
- ✓ Documentația inițială (acest README + analysis.md)
- ✓ Studiul algoritmilor de drum minim
- ✓ Modelarea problemei
- [ ] Revizuire și feedback

**Deliverables:**
- Structura proiectului
- README.md complet
- analysis.md cu detalii teoretice
- Diagrame UML preliminare

---

### **SĂPTĂMÂNA 2-3: Implementare Data Structures** (26 martie - 6 aprilie)
- [ ] Implementarea clasei `Node`
- [ ] Implementarea clasei `Edge`
- [ ] Implementarea clasei `Graph`
- [ ] Teste unitare pentru structuri de date
- [ ] Parsare date din fișiere

**Deliverables:**
- Modulele `src/models/` complet implementate
- `src/graph.py` funcțional
- Test coverage > 80%

---

### **SĂPTĂMÂNA 4-5: Implementare Algoritmi** (9-20 aprilie)
- [ ] Algoritmul Dijkstra cu priority queue
- [ ] Algoritmul Bellman-Ford cu detecție cicluri negative
- [ ] Algoritmul A* cu heuristica euclidiană
- [ ] Teste exhaustive pentru fiecare algoritm
- [ ] Benchmark și măsurări de performanță

**Deliverables:**
- Fișierele `dijkstra.py`, `bellman_ford.py`, `astar.py`
- Suite de teste cuprinzătoare
- Raport de performanță

---

### **SĂPTĂMÂNA 6: Interfață și Vizualizare** (23-27 aprilie)
- [ ] Interfață în linie de comandă (CLI)
- [ ] Vizualizare grafuri cu Matplotlib
- [ ] Afișare rute calculate
- [ ] Statistici și timings
- [ ] Validare și corectare bug-uri

**Deliverables:**
- `src/main.py` funcțional
- `src/utils/visualization.py` complet
- Demo executabil

---

### **SĂPTĂMÂNA 7: Testare și Optimizare** (30 aprilie - 4 mai)
- [ ] Teste comprensive (unitare, integrare, stress)
- [ ] Profilare și optimizare performanță
- [ ] Refactoring cod pentru claritate
- [ ] Documentare cod inline
- [ ] Tratare cazuri extreme

**Deliverables:**
- Test coverage > 90%
- Raport de optimizare
- Cod refactorat

---

### **SĂPTĂMÂNA 8: Documentație Finală și Prezentare** (7-11 mai)
- [ ] Completare documentație API
- [ ] Ghid de utilizare detailat
- [ ] Analiza comparativă finală
- [ ] Prezentare și demo
- [ ] Pregătire pentru evaluare

**Deliverables:**
- Documentație API completă (docstrings Python)
- Tutorial de utilizare
- Raport final de analiză
- Material pentru prezentare

---

## 6. Structura Fișierelor

```
sistem_de_navigatie/
│
├── src/                           # Cod sursă
│   ├── __init__.py
│   ├── main.py                    # Punct de intrare - aplicația principală
│   ├── graph.py                   # Clasă pentru gestiunea grafului
│   │
│   ├── models/                    # Structuri de date
│   │   ├── __init__.py
│   │   ├── node.py               # Definiția clasei Node
│   │   ├── edge.py               # Definiția clasei Edge
│   │   └── route.py              # Definiția clasei Route (rezultat)
│   │
│   ├── algorithms/                # Algoritmi de drum minim
│   │   ├── __init__.py
│   │   ├── dijkstra.py           # Implementarea algoritmului Dijkstra
│   │   ├── bellman_ford.py       # Implementarea algoritmului Bellman-Ford
│   │   └── astar.py              # Implementarea algoritmului A*
│   │
│   └── utils/                     # Funcții utilitare
│       ├── __init__.py
│       ├── parser.py             # Parsare fișiere de date
│       └── visualization.py      # Vizualizare grafuri cu Matplotlib
│
├── tests/                         # Suite de teste
│   ├── __init__.py
│   ├── test_models.py            # Teste pentru structuri de date
│   ├── test_graph.py             # Teste pentru gestiunea grafului
│   └── test_algorithms.py        # Teste pentru algoritmi
│
├── data/                          # Fișiere de date și grafuri
│   ├── city_graph.txt            # Reprezentare a unui graf de oraș
│   └── test_cases.txt            # Cazuri de test cu rezultate așteptate
│
├── docs/                          # Documentație suplimentară
│   ├── analysis.md               # Analiza teoretică detaliată
│   └── implementation_notes.md   # Note de implementare
│
├── README.md                      # Acest fișier
├── requirements.txt               # Dependențele Python
└── .gitignore                     # Fișiere ignorate de Git
```

---

## 7. Criterii de Evaluare

### Cod și Implementare (40%)
- Corectitudinea algoritmilor
- Complianță cu structura proiectului
- Stil cod și convenții Python (PEP 8)
- Documentare cod (docstrings)

### Testare (20%)
- Coverage de teste (minim 80%)
- Teste exhaustive și cazuri extreme
- Rapoarte de bug și corectii

### Documentație (20%)
- Claritate și completitudine
- Analiza teoretică detaliată
- Diagramele și vizualizările

### Performanță și Analiza (20%)
- Complexitate corect calculată
- Comparație exactă între algoritmi
- Identificare cazuri de utilizare ideale

---

## 8. Cum se Folosește Acest Proiect

### 8.1 Instalare

```bash
# Clonare repository (ulterior)
git clone <repository-url>
cd sistem_de_navigatie

# Creare mediu virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# sau
venv\Scripts\activate  # Windows

# Instalare dependențe
pip install -r requirements.txt
```

### 8.2 Executare

```bash
# Rulare aplicație principală
python src/main.py

# Rulare teste
python -m pytest tests/
# sau
python -m unittest discover -s tests -p "test_*.py"
```

### 8.3 Structura Date (city_graph.txt)

Format de intrare pentru definirea unui graf (vor fi detalii în săptămâna 2):
```
HEAD_GRAPH
noduri: 5
0 Piata Ovidiu
1 Piata Civica
2 Parc Central
3 Gara Centrala
4 Teatru
muchii:
0 1 450
1 2 320
2 3 680
3 4 250
0 3 950
```

---

## 9. Referințe și Resurse

### Materiale de Studiu
- **Cormen, Leiserson, Rivest, Stein** - "Introduction to Algorithms" (CLRS)
- **Sedgewick, Wayne** - "Algorithms, 4th Edition"
- **Dijkstra, E. W.** - "A Note on Two Problems in Connexion with Graphs" (1959)

### Documentație Online
- [NetworkX Documentation](https://networkx.org/)
- [Matplotlib Gallery](https://matplotlib.org/gallery.html)
- [Python Official Documentation](https://docs.python.org/3/)

### Instrumente Online
- [Visualgo.net](https://visualgo.net/) - Vizualizare algoritmi
- [Graph Online](https://graphonline.ru/) - Editor grafuri

---

## 10. Contact și Suport

**Autor:** [Completezi cu numele tău]  
**Data Creării:** Martie 2026  
**Ultimă Actualizare:** 3 martie 2026

---

**Status:** ✅ Proiect în faza de analiză și planificare
