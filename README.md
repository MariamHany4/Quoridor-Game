# 🎲 Quoridor Game
---

## 🌟 Overview

**Quoridor Game** is a complete implementation of the classic **2-player Quoridor board game** built as a **desktop application using PyQt**.  
The game features a modern graphical interface, intelligent AI opponents, and full enforcement of official game rules.

Players can move pawns, place walls strategically, and challenge either another human player or an AI with multiple difficulty levels.

---

## 🏁 Game Rules Summary

| Feature | Description |
|--------|------------|
| Board | 9×9 grid |
| Players | 2 |
| Pawns & Walls | Each player starts with 1 pawn and 10 walls |
| Objective | Reach the opposite side of the board first |
| Pawn Movement | One square orthogonally; jump over adjacent opponent pawn if possible |
| Wall Placement | Two squares long; cannot overlap, cross, or block all paths |

---

## 🚀 Features

### Core Features
- Full 2-player gameplay following official rules 📜  
- Human vs Human mode 🤝  
- Human vs AI mode 🤖  
- Multiple AI difficulty levels  
- Complete rule validation and illegal move prevention ✅  
- Pathfinding ensures no player is ever fully blocked 🔀  

### User Interface (PyQt)
- Modern PyQt-based desktop GUI 🖥️  
- Click-based pawn movement and wall placement 🖱️  
- Custom window design with animations and shadows ✨  
- Turn indicator and remaining wall count ⏱️  
- Winner announcement and game state messages 💬  
- Return to main menu / reset game functionality 🔄  

### Bonus Features (Optional)
- Undo / Redo moves ↩️  
- Save & Load game state 💾  
- Extendable to larger boards or 4-player mode 🛠️  

---

## 🧠 AI Opponent

| Difficulty | Behavior |
|-----------|----------|
| Easy | Random valid moves |
| Medium | Shortest-path evaluation with basic wall strategy |
| Hard | Minimax with Alpha-Beta pruning and path heuristics |

---

## 🎮 Controls

| Action | How to Perform |
|------|---------------|
| Move Pawn | Click your pawn → Click highlighted square |
| Place Wall | Select wall mode → Click a valid edge |
| Reset Game | Click **Reset** button |
| Back to Menu | Click **Back** button |

---

## 🛠️ Installation

### Requirements
- Python **3.11+**
- **PyQt5**

Install dependencies:
```bash
pip install PyQt5
