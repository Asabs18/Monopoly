# 🎲 Monopoly Game

A fully functional multiplayer Monopoly game built with **Python** and **Pygame**, supporting up to 4 players with trading, auctions, property management, and a custom graphical interface.

> 💻 Language: **Python**  
> 🎮 Category: **Game**



## 🚀 Features

- 🎨 **Custom Graphical User Interface**  
  Built with Pygame, the game includes dynamic UI components, responsive layouts, and pixel-perfect positioning for player pieces, properties, dice, and more.

- 💰 **Full Monopoly Mechanics**  
  Includes buying/selling properties, property sets, rent handling, chance/community chest, houses/hotels, mortgages, and bankruptcy logic.

- 🔄 **Trading System (To be fully implemented)**  
  In-game trading interface allows players to exchange properties and cash.

- 🏦 **Auction Mode**  
  Properties can be auctioned off when players choose not to buy them.

- 👥 **Multiplayer Support**  
  Supports 2 to 4 players on the same device, each with their own controls and profile.

- 🔧 **Modular Architecture**  
  Custom internal API handles the communication between GUI elements and game logic for maintainable and scalable code.



## 📁 Project Structure (Overview)

```
Monopoly/
├── Assets/
│ ├── examples/ # Sample assets by color group
│ ├── fonts/ # Custom font files
│ └── images/ # Game art assets
│   ├── board/ # Board images
│   ├── cards/ # Property & chance cards
│   ├── dice/ # Dice graphics
│   └── pieces/ # Player piece icons
│
├── src/
│ ├── config/ # UI configuration (e.g., displayAssets.py, fontAssets.py)
│ ├── game/ # Core game logic (turns, movement, property handling)
│ └── ui/
│   ├── components/ # UI components like buttons, labels, inputs
│   └── menus/ # Game menus (start, settings, etc.)
│
├── main.py # Entry point to launch the game
└── README.md # Project documentation
```

## 📦 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/Asabs18/Monopoly.git
   cd Monopoly
   ```

2. **Install dependencies**

    ```bash
    pip install pygame
    ```

3. **Run the game**

    ```bash
    python main.py
    ```

## 🙋‍♂️ Author
```
Aidan Sabatini

GitHub: @Asabs18
```