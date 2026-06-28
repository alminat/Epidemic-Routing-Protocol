# Epidemic Routing Protocol – NS-3 Simulacija

> Simulacija i analiza Epidemic Routing protokola u NS-3 simulatoru za DTN mreže  


## 📌 O projektu

Ovaj projekat istražuje performanse **Epidemic Routing protokola** u mrežama otpornim na kašnjenje (Delay-Tolerant Networks – DTN). Epidemic routing jedan je od prvih i najznačajnijih algoritama baziranih na replikaciji podataka, koji koristi **Store-Carry-Forward** mehanizam za prenos poruka u okruženjima bez stalne mrežne povezanosti.

Projekt se sastoji od dva dijela:
- **Teorijski dio** – analiza arhitekture DTN mreža, principa rada Epidemic protokola i poređenje sa srodnim protokolima (Spray and Wait, PRoPHET)
- **Praktični dio** – implementacija i simulacija u NS-3 okruženju kroz više scenarija


## 📁 Struktura repozitorijuma

```
Epidemic-Routing-Protocol/
│
├── scenariji/
│   ├── prvi_scen.csv
│   ├── scenarij2_hopcount.csv
│   ├── treci_scenarij_broj_cvorova.csv
│   └── manual_results.csv
│
├── kod/
│   ├── I-scenariji/
│   │   └── scenarij1_queue_length.py
│   ├── II-scenariji/
│   │   └── scenarij2_hopcount.py
│   ├── III-scenariji/
│   │   └── scenarij3_broj_cvorova.py
│   └── IV-scenariji/
│       └── scenarij4_svi.py
│
├── grafici/
│   ├── I-scenariji/
│   │   └── scenarij1_queue_length.png
│   ├── II-scenariji/
│   │   └── scenarij2_hopcount.png
│   ├── III-scenariji/
│   │   └── scenarij3_broj_cvorova.png
│   └── IV-scenariji/
│       ├── scenarij4_1_queue_hop.png
│       ├── scenarij4_2_nodes_queue.png
│       └── scenarij4_3_nodes_hop.png
│
├── izvjestaji/
│   └── KUTM.pdf
│
└── README.md
```

---

## 🔬 Simulacijski scenariji

Simulacija je provedena na modelu DTN mreže sa **50 mobilnih čvorova** u prostoru dimenzija 1500 m × 300 m, uz korištenje Random Waypoint modela mobilnosti.

### Scenarij 1 – Uticaj veličine bafera (Queue Length)

- Parametar `queueLength` mijenjan u opsegu od 0 do 2000 paketa
- **Najbolji rezultat:** Delivery Ratio = **32.4%** pri `queueLength = 1200`

![Scenarij 1](grafici/I-scenariji/scenarij1_queue_length.png)

---

### Scenarij 2 – Uticaj broja skokova (Hop Count)

- Parametar `hopCount` mijenjan u opsegu od 1 do 50
- **Najbolji rezultat:** Delivery Ratio = **30.0%** pri `hopCount = 29`

![Scenarij 2](grafici/II-scenariji/scenarij2_hopcount.png)

---

### Scenarij 3 – Uticaj broja čvorova

- Parametar `nWifis` mijenjan u opsegu od 5 do 100 čvorova
- **Najbolji rezultat:** Delivery Ratio = **27.8%** pri `nWifis = 45`

![Scenarij 3](grafici/III-scenariji/scenarij3_broj_cvorova.png)

---

### Scenarij 4 – Kombinovani uticaj parametara

| Podscenarij | Optimalni parametri | Max Delivery Ratio | Min Packet Loss |
|---|---|---|---|
| 4.1 – Bafer + Hop Count | queueLength=1000, hopCount=200 | 26.6% | 73.4% |
| 4.2 – Čvorovi + Bafer | nWifis=30, queueLength=3000 | 37.8% | 62.2% |
| 4.3 – Čvorovi + Hop Count | nWifis=30, hopCount=65 | **39.0%** | **61.0%** |

![Podscenarij 4.1](grafici/IV-scenariji/4.1.jpg)
![Podscenarij 4.2](grafici/IV-scenariji/4.2.jpg)
![Podscenarij 4.3](grafici/IV-scenariji/4.3.jpg)

---

## 📊 Ključni zaključci

- Povećanje kapaciteta bafera poboljšava performanse do određene granice, nakon koje dolazi do zasićenja
- Optimalan broj čvorova za posmatrani scenarij iznosi **30–45**, nakon čega intenzivna replikacija degradira performanse
- Kombinovana optimizacija više parametara daje bolje rezultate od optimizacije jednog parametra
- **Packet loss** u svim scenarijima ostaje iznad 60%, što je karakteristika Epidemic Routing protokola zbog intenzivnog "plavljenja" (flooding overhead)
- Rezultati su konzistentni s teorijskim SI modelom širenja poruka

---

## 📄 Dokumentacija

- [Teorijski izvještaj](izvjestaji/KUTM.pdf)
- [Praktični izvještaj](izvjestaji/KUTM_prakticni_dio.pdf)

---

## 📚 Literatura

1. Vahdat, A. and Becker, D. (2000). *Epidemic routing for partially connected ad hoc networks.* Duke University.
2. Herbrant, *Epidemic Routing ns-3 Benchmark Implementation*, GitHub.
3. Fall, K. (2003). *A delay-tolerant network architecture for challenged internets.* SIGCOMM.
4. Spyropoulos et al. (2005). *Spray and Wait.* ACM SIGCOMM.
5. Lindgren et al. (2003). *PRoPHET: Probabilistic routing in intermittently connected networks.* ACM SIGMOBILE.
6. Yulianti et al. (2020). *Performance comparison of epidemic, prophet, spray and wait, binary spray and wait, and prophetv2.* UTM Malaysia.
