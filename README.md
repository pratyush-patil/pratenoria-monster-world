# Pratenoria — Monster World

> Pick a starter, master the type triangle, and battle your way across the map to stop **LINOX** before he steals the world's strongest Pratemon.

Pratenoria is a single-player, turn-based monster-battling game with a retro, terminal-style look. Choose one of nine Pratemons, fight rival trainers across the journey map, and face Linox and his mysterious Dark-type, Shadowfang, in the final battle.

## Features

- **9 Pratemons** across three elements: Fire, Water and Earth
- **Type triangle:** Fire beats Earth, Earth beats Water, Water beats Fire
- **Journey map** with 5 checkpoints, from Beginnings to Linox's Lair
- **Turn-based battles** with scratch attacks, skills and switching Pratemons
- **Team and Dex screens** to manage your roster and browse every Pratemon
- **Resizable window** that adjusts to maximize and minimize
- **Story** told by Professor Pratty, with Linox as the villain

## How to Run

1. Install [Python 3](https://www.python.org/downloads/) (Tkinter comes with it on Windows and Mac).
2. Install the image library:
   ```
   pip install Pillow
   ```
3. Download or clone this repo, and keep `finalversion.py` and the `images` folder in the same directory.
4. Start the game:
   ```
   python finalversion.py
   ```

## Project Structure

```
.
├── finalversion.py   # the game
└── images/           # monster and character artwork (PNG)
```

The game loads artwork from `images/` by exact filename. If an image is missing, it shows a colored placeholder instead, so the game still runs.

## How to Play

1. Pick a starter Pratemon and meet Professor Pratty.
2. Open the **Battle** screen and choose a checkpoint on the journey map.
3. In battle, use the type triangle to pick strong matchups. Strong attacks deal 1.5x damage and weak ones deal 0.5x.
4. Win battles to grow your team, then take on Linox at the end of the trail.

The **Help** screen in the game shows the full type chart.

## Built With

- Python
- Tkinter
- Pillow

## Credits

Pratyush
