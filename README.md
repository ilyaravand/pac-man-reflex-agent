# Pac‑Man — Reflex & Multi‑Agent Search

Pac‑Man agents implemented on top of the classic UC Berkeley **CS188 Project 2 (Multi‑Agent Search)**.  
This repo focuses on a stronger **ReflexAgent** and **Minimax**, **Alpha‑Beta**, and **Expectimax** agents with a custom evaluation function.

> ⚠️ Educational use only. This project mirrors the CS188 structure so you can experiment locally. Please keep the original attribution and don’t republish course solutions.

---

## 🎮 What’s inside

- **ReflexAgent** with an improved action score:
  - prefers food‑closer moves,
  - avoids non‑scared ghosts,
  - opportunistically chases **scared** ghosts,
  - small penalty for `Stop`.
- **Minimax**, **Alpha‑Beta**, **Expectimax** with a tuned evaluation function.
- Standard CS188 Pac‑Man engine: `pacman.py`, `game.py`, `ghostAgents.py`, `util.py`, `layouts/`.

---

## 🚀 Quickstart

### Requirements
- Python 3.8+ (no extra packages required)

### Install / Run
```bash
git clone https://github.com/ilyaravand/pac-man-reflex-agent
cd pac-man-reflex-agent
```

Play a human game:
```bash
python pacman.py
```

---

## 🧠 Run the agents

**ReflexAgent**
```bash
# Small classic layout
python pacman.py -p ReflexAgent -l smallClassic

# Faster animation, 2 ghosts
python pacman.py -p ReflexAgent -l testClassic -k 2 --frameTime 0
```

**Minimax** *(if implemented)*
```bash
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=3
```

**Alpha‑Beta** *(if implemented)*
```bash
python pacman.py -p AlphaBetaAgent -l smallClassic -a depth=3
```

**Expectimax** *(if implemented)*
```bash
python pacman.py -p ExpectimaxAgent -l smallClassic -a depth=2
```

### Common flags
- `-p <AgentName>`: which agent to run  
- `-l <layout>`: map (e.g., `tinyClassic`, `testClassic`, `smallClassic`, `mediumClassic`)  
- `-k <N>`: number of ghosts  
- `-a key=value`: pass agent params (e.g., `depth=3`)  
- `--frameTime 0`: fast animation  
- `-n <N>`: run multiple games  
- `-q` / `--no-graphics`: quiet/headless mode  
- `-f`: fixed random seed (reproducible)

---

## 🗂️ Project structure (key files)

```
pac-man-reflex-agent/
├─ multiAgents.py        # Reflex / Minimax / Alpha-Beta / Expectimax + eval fn
├─ pacman.py             # Main runner & CLI
├─ game.py               # Core engine
├─ ghostAgents.py        # Ghost behaviors
├─ util.py               # Helpers & data structures
├─ layouts/              # Map files (e.g., tinyClassic.lay)
└─ test_cases/, autograder.py
```


---

## 🔍 Implementation notes (high level)

- **ReflexAgent evaluation** balances:
  - distance to nearest food (inverse Manhattan),
  - distance to nearest **non‑scared** ghost (avoid),
  - scared timers (seek ghosts if safe),
  - small negative for `Stop` or moving into danger tiles.
- **Search agents** treat a full *ply* as one Pac‑Man move followed by all ghosts.
  - **Minimax**: worst‑case adversaries.
  - **Alpha‑Beta**: same values as Minimax with pruning.
  - **Expectimax**: stochastic ghosts (chance nodes), maximizing **expected** value.

---

## ✅ Autograder 

```bash
# Run everything
python autograder.py

# Run a specific question (e.g., q2 Minimax)
python autograder.py -q q2

# Inspect a particular test
python autograder.py -t test_cases/q2/0-small-tree
```

Add `--graphics` / `--no-graphics` as needed.

---

## 🙏 Acknowledgements

This work is based on the **UC Berkeley CS188 Pac‑Man AI Projects** (Project 2: Multi‑Agent Search).  
The original projects were developed at UC Berkeley. Please retain attribution and follow course policies.

- CS188 home: https://inst.eecs.berkeley.edu/~cs188/
- Project 2 (reference spec): https://inst.eecs.berkeley.edu/~cs188/fa24/projects/proj2/

---

## 📝 License

This repo is shared for learning and portfolio purposes.  
Respect the CS188 license/attribution and your institution’s academic integrity policies.

---

## 📬 Contact

Questions or ideas?  
**Ilya Ravand** — <ilyaravand@gmail.com>
