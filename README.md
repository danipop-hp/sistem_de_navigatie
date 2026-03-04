# Analiză - Algoritmi de Drum Minim

## 1. Problema Drumului Minim

Dat graf ponderat $G = (V, E)$ cu funcție pondere $w: E \rightarrow \mathbb{R}^+$, găsim drumul minim de la sursă $s$ la destinație $t$.

Variante:
- Single Source: O sursă, toate destinațiile (Dijkstra, Bellman-Ford)
- Single Pair: O pereche sursă-destinație (A*, Dijkstra)
- All Pairs: Toate perechile (Floyd-Warshall)
- Ponderi negative: Bellman-Ford

## 2. Reprezentări ale Grafului

Lista de adiacență: $O(V + E)$ memorie, lentă pentru verificare muchii
Matrice: $O(V^2)$ memorie, acces $O(1)$ la orice muchie  

Grafurile urbane sunt rare, deci lista de adiacență e preferată.

## 3. Algoritmi

### 3.1 Dijkstra

Principiu: Greedy - explorează nodurile cel mai apropiat de sursă
Complexitate: $O((V+E)\log V)$ cu priority queue, $O(V^2)$ cu matrice
Ponderi: Doar pozitive
Cazuri: Google Maps, OSPF routing

Pseudocod:
```
DIJKSTRA(G, s):
  dist[s] = 0, dist[v] = ∞ pentru v ≠ s
  Q = priority_queue([toate nodurile])
  
  cât timp Q nu e vidă:
    u = Q.pop_min()
    pentru fiecare (u, v) cu pondere w:
      dacă dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
        Q.decrease_key(v)
  
  returnează dist
```

3.2 Bellman-Ford

Principiu: Relaxare iterativă - repeți actualizări până convergență
Complexitate: $O(V \times E)$
Ponderi: Pozitive și negative
Detectează: Cicluri negative
Cazuri: RIP routing, detecție arbitraj valutar

Pseudocod:
```
BELLMAN_FORD(G, s):
  dist[s] = 0, dist[v] = ∞ pentru v ≠ s
  
  pentru i = 1 la V-1:
    pentru fiecare muchie (u, v) cu pondere w:
      dacă dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
  
  # Detectare ciclu negativ
  pentru fiecare muchie (u, v) cu pondere w:
    dacă dist[u] + w < dist[v]:
      returnează "Ciclu negativ!"
  
  returnează dist
```

3.3 A* (A-Star)

Principiu: Dijkstra cu ghidaj heuristic - prioritizează noduri vers destinație
Complexitate: $O(E)$ în practică cu heuristic bună
Ponderi: Doar pozitive
Cazuri: GPS (Google Maps, Waze), pathfinding jocuri video  

Funcția de evaluare:
$$f(n) = g(n) + h(n)$$
unde $g(n)$ = cost real de la sursă, $h(n)$ = estimare la destinație

Heuristici:
- Euclidiană: $h = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$
- Manhattan: $h = |x_2-x_1| + |y_2-y_1|$

Pseudocod:
```
A_STAR(G, s, t, h):
  g[s] = 0, f[s] = h(s, t)
  deschis = {s}, inchis = {}
  
  cât timp deschis nu e vidă:
    u = nod din deschis cu min f
    
    dacă u == t:
      returnează drum
    
    inchis.add(u)
    pentru fiecare vecin v al lui u:
      g_nou = g[u] + w(u, v)
      dacă v ∉ inchis și g_nou < g[v]:
        g[v] = g_nou
        f[v] = g[v] + h(v, t)
        deschis.add(v)
  
  returnează "Nu e drum"
```



## 4. Complexitate

| Algoritm | Timp | Memorie | Ponderi Negative | Cicluri Negative |
|---|---|---|---|---|
| Dijkstra (PQ) | $O((V+E)\log V)$ | $O(V+E)$ | Nu | Nu |
| Dijkstra (Matrice) | $O(V^2)$ | $O(V^2)$ | Nu | Nu |
| Bellman-Ford | $O(V \times E)$ | $O(V+E)$ | Da | Da |
| A* | $O(E)$ practică | $O(V)$ | Nu | Nu |

Analiza:
- Dijkstra exploatează $V$ noduri (extrage minim) + relaxează $E$ muchii = $O((V+E)\log V)$
- Bellman-Ford face $V-1$ runde de $E$ relaxări = $O(VE)$
- A* exploatează mai puține noduri cu heuristic bună → mai rapid în practică

5. Alegere Algoritm

| Scenariu | Algoritm |
| O sursă, toate destinațiile, ponderi pozitive | Dijkstra |
| Ponderi negative, detecție cicluri | Bellman-Ford |
| O pereche sursă-destinație, ponderi pozitive | A* |
| Toate perechile, ponderi pozitive | Floyd-Warshall |

6. Extensii Viitoare

- All-Pairs Shortest Paths: Floyd-Warshall $O(V^3)$
- K-shortest paths: Găsire a k-lea cel mai scurt drum
- Drum minim cu restricții: Ocolire zone, trecere prin puncte
- Ponderi dinamice: Trafic în timp real
- Problema rutării vehiculelor: Multiple vehicule, clienți
- Rutare multimodală: Mașină + metrou + bicicletă
- ML-optimizare: Rețele neuronale + RL pentru rutare

7. Concluzii

1. Dijkstra: Cel mai bun pentru grafuri urbane (ponderi pozitive)
2. Bellman-Ford: Necesar pentru ponderi negative
3. A*: Performanță maximă practică; folosit în GPS

